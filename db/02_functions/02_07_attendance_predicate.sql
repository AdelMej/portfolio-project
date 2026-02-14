create or replace function app_fcn.is_attendance_open(
	p_session_id uuid
)
returns boolean
language sql
stable
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_attendance_open
	 *
	 * Determines whether attendance is currently open for a session.
	 *
	 * Domain rule:
	 *   - Attendance opens when the session starts
	 *   - Attendance is not open if the session is cancelled
	 *
	 * This function does NOT consider session end time.
	 * Closing attendance is a separate domain decision.
	 *
	 * Parameters:
	 *   p_session_id - Identifier of the session to check
	 *
	 * Returns:
	 *   TRUE  if the session exists, is not cancelled, and has started
	 *   FALSE otherwise
	 *
	 * Usage:
	 *   Used as a predicate to enforce attendance lifecycle invariants
	 *   at the database boundary.
	 */
	SELECT EXISTS(
		SELECT 1
		FROM app.sessions
		WHERE id = p_session_id
			AND cancelled_at IS NULL
			AND now() >= starts_at
		
	);
$$;

COMMENT ON FUNCTION app_fcn.is_attendance_open(uuid) IS
'Predicate function determining whether attendance is open for a session.
Attendance opens when the session start time is reached and the session
is not cancelled. Session end time is intentionally ignored to keep
attendance lifecycle rules explicit and composable.';


create or replace function app_fcn.is_session_attended(
	p_session_id uuid
)
returns boolean
language sql
STABLE
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_attended
	 *
	 * Predicate that returns true if the given session
	 * has at least one attendance record.
	 *
	 * This represents the domain fact that attendance
	 * has started for the session.
	 *
	 * Domain invariants:
	 *   - Once a session is attended, pre-attendance
	 *     operations must no longer be allowed.
	 *
	 * Notes:
	 *   - This is a pure predicate (no side effects)
	 *   - Intended to be used under an advisory lock
	 *   - Used to enforce idempotent, race-safe workflows
	 */
	SELECT EXISTS (
		SELECT 1
		FROM app.session_attendance
		WHERE session_id = p_session_id
	);
$$;

COMMENT ON FUNCTION app_fcn.is_session_attended(uuid) IS
'Predicate that returns true if a session has at least one attendance record.
Represents the domain fact that attendance has started.
Used to enforce invariants such as disabling pre-attendance once attendance exists.';


CREATE OR REPLACE FUNCTION app_fcn.is_attendance_payload_valid(
    p_session_id uuid,
    p_attendance jsonb
)
RETURNS boolean
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.is_attendance_payload_valid
 *
 * Validates the integrity of an attendance payload for a session.
 *
 * The payload is expected to be a JSON array of objects:
 *   [{ "user_id": uuid, "attended": boolean }, ...]
 *
 * Validation rules:
 *   - No duplicate user_id
 *   - All user_id belong to paid, non-cancelled participants
 *   - Attendance has not already been recorded for the session
 *
 * Notes:
 *   - The "attended" boolean is intentionally ignored for validation
 *   - This function performs no writes
 */
DECLARE
    invalid boolean;
BEGIN
	IF NOT app_fcn.is_coach() THEN
		RAISE EXCEPTION 'permission denied'
			USING ERRCODE = 'AP401';
	END IF;
	
    -- Attendance must not already exist
    IF app_fcn.is_attended(p_session_id) THEN
        RETURN FALSE;
    END IF;

	IF app_fcn.current_user_id() IS NULL THEN
	    RAISE EXCEPTION 'missing actor context'
	        USING ERRCODE = 'AP401';
	END IF;

	IF jsonb_array_length(p_attendance) = 0 THEN
	    RAISE EXCEPTION 'attendance payload must not be empty'
	        USING ERRCODE = 'AP422';
	END IF;

    WITH input AS (
        SELECT
            r.user_id
        FROM jsonb_to_recordset(p_attendance) AS r(
            user_id uuid,
            attended boolean
        )
    )
    SELECT EXISTS (
        -- duplicate users
        SELECT 1
        FROM (
            SELECT user_id
            FROM input
            GROUP BY user_id
            HAVING COUNT(*) > 1
        ) dup

        UNION ALL

        -- users not eligible for attendance
        SELECT 1
        FROM input i
        LEFT JOIN app.session_participation sp
            ON sp.user_id = i.user_id
           AND sp.session_id = p_session_id
           AND sp.cancelled_at IS NULL
           AND sp.paid_at IS NOT NULL
        WHERE sp.user_id IS NULL
    )
    INTO invalid;

    RETURN NOT invalid;
END;
$$;

COMMENT ON FUNCTION app_fcn.is_attendance_payload_valid(uuid, jsonb) IS
'Validates an attendance payload by ensuring all user_ids are unique,
belong to paid and non-cancelled participants of the session,
and that attendance has not already been recorded.
The attended flag is ignored during validation.';


