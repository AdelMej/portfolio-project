	p_session_id uuid
)
returns table(
	user_id uuid,
	first_name text,
	last_name text
)
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.get_pre_attendance
	 *
	 * Returns the list of participants eligible for attendance
	 * for a given session, before attendance has started.
	 *
	 * This function represents the "pre-attendance" phase of
	 * the session lifecycle.
	 *
	 * Domain invariants:
	 *   - Only coaches may access pre-attendance data
	 *   - Once a session is attended, pre-attendance is no longer available
	 *   - Only paid and non-cancelled participants are returned
	 *
	 * Concurrency:
	 *   - Uses an advisory transaction lock scoped to the session
	 *     to ensure race safety with attendance creation
	 *
	 * Idempotency:
	 *   - If attendance already exists, returns an empty result set
	 *     without raising an error
	 */
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('session:' || p_session_id::text)
		);

		IF NOT app_fcn.is_coach() THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		-- Pre-attendance is invalid once attendance has started
		IF app_fcn.is_session_attended(p_session_id) THEN
			RETURN;
		END IF;

		RETURN QUERY
		SELECT
			up.user_id,
			up.first_name::text,
			up.last_name::text
		FROM app.session_participation sp
		JOIN app.user_profiles up
			ON up.user_id = sp.user_id
		WHERE sp.session_id = p_session_id 
			AND sp.cancelled_at IS NULL
			AND sp.paid_at IS NOT NULL;
	END;
$$;

COMMENT ON FUNCTION app_fcn.get_pre_attendance(uuid) IS
'Returns the list of paid, non-cancelled participants eligible for attendance
before attendance has started for a session.
Enforces domain invariants via authorization checks, attendance-state predicates,
and advisory transaction locking.';

CREATE OR REPLACE FUNCTION app_fcn.create_attendance(
    p_session_id uuid,
    p_attendance jsonb
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.create_attendance
 *
 * Records attendance for a session.
 *
 * Preconditions (enforced here):
 *   - Caller must be a coach
 *   - Session must exist and not be cancelled
 *   - Attendance window must be open
 *   - Attendance must not already exist
 *   - Attendance payload must be valid
 *
 * Concurrency:
 *   - Uses an advisory transaction lock scoped to the session
 *
 * Persistence:
 *   - Append-only insert into session_attendance
 */
BEGIN
    -- race safety
    PERFORM pg_advisory_xact_lock(
        hashtext('session:' || p_session_id::text)
    );

    IF NOT app_fcn.is_coach() THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    IF NOT app_fcn.session_exists(p_session_id) THEN
        RAISE EXCEPTION 'session not found'
            USING ERRCODE = 'AP404';
    END IF;

    IF app_fcn.is_session_cancelled(p_session_id) THEN
        RAISE EXCEPTION 'session cancelled'
            USING ERRCODE = 'AP409';
    END IF;

    IF NOT app_fcn.is_attendance_open(p_session_id) THEN
        RAISE EXCEPTION 'attendance not open'
            USING ERRCODE = 'AB409';
    END IF;

    IF app_fcn.is_session_attended(p_session_id) THEN
        RETURN;
    END IF;

    IF NOT app_fcn.is_attendance_payload_valid(p_session_id, p_attendance) THEN
        RAISE EXCEPTION 'invalid attendance payload'
            USING ERRCODE = 'AP422';
    END IF;

    INSERT INTO app.session_attendance (
		id,
        session_id,
        user_id,
        attended,
        recorded_at,
		recorded_by
    )
    SELECT
		gen_random_uuid(),
        p_session_id,
        r.user_id,
        r.attended,
        now(),
		current_setting('app.current_user_id')::uuid
    FROM jsonb_to_recordset(p_attendance) AS r(
        user_id uuid,
        attended boolean
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.create_attendance(uuid, jsonb) IS
'Creates attendance records for a session in an append-only manner.
Enforces authorization, session state, time window, payload integrity,
and race safety via advisory locking.';

CREATE OR REPLACE FUNCTION app_fcn.fetch_attendance_list(
    p_session_id uuid
)
RETURNS TABLE(
    user_id uuid,
    first_name text,
    last_name text,
    attended boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
BEGIN
    /*
     * Returns the attendance list for a given session.
     *
     * This function is restricted to administrators only.
     * It returns all users associated with the session along with
     * their attendance status.
     *
     * Columns returned:
     * - user_id   : UUID of the user
     * - first_name: User's first name
     * - last_name : User's last name
     * - attended  : Whether the user attended the session
     *
     * Used for administrative oversight and reporting.
     */
    IF NOT app_fcn.is_admin() THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    RETURN QUERY
        SELECT
            up.user_id,
            up.first_name::text,
            up.last_name::text,
            sa.attended
        FROM app.user_profiles up
        JOIN app.session_attendance sa
            ON up.user_id = sa.user_id
        WHERE sa.session_id = p_session_id;
END;
$$;

COMMENT ON FUNCTION app_fcn.fetch_attendance_list(uuid)
IS
'Admin-only function that returns the attendance list for a session.
Includes user identity information and attendance status.
Used for administrative reporting and oversight.';