create or replace function app_fcn.get_pre_attendance(
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
		IF app_fcn.is_attended(p_session_id) THEN
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
