\c app

CREATE OR replace function app_fcn.is_session_full(
	p_session_id uuid,
	p_capacity int
)
returns boolean
language sql
stable
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_full
	 *
	 * Determines whether a session has reached its maximum capacity.
	 *
	 * A session is considered "full" when the number of active
	 * (non-cancelled) participations is greater than or equal to
	 * the provided capacity.
	 *
	 * Derived state:
	 *   - Only participations with cancelled_at IS NULL are counted
	 *
	 * Usage:
	 *   - Registration eligibility checks
	 *   - Capacity enforcement before creating participation
	 *
	 * Notes:
	 *   - Does not acquire locks
	 *   - Intended to be called under an advisory transaction lock
	 *     by the write-side function enforcing registration invariants
	 */
	SELECT count(*) >= p_capacity
	FROM app.session_participation
	WHERE session_id = p_session_id
		AND cancelled_at IS NULL
		AND (
			paid_at IS NOT NULL
			OR expires_at > now()
		)
$$;

COMMENT ON FUNCTION app_fcn.is_session_full(uuid, int) IS
'Returns true if the number of active (non-cancelled) participations
for a session has reached or exceeded the given capacity.';


create or replace function app_fcn.has_active_participation(
	p_user_id uuid,
	p_session_id uuid
)
returns boolean
language sql
stable
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.has_active_participation
	 *
	 * Determines whether a user already has an active participation
	 * for a given session.
	 *
	 * A participation is considered active when:
	 *   - session_id matches
	 *   - user_id matches
	 *   - cancelled_at IS NULL
	 *
	 * Derived state:
	 *   - Uses session_participation as the source of truth
	 *
	 * Usage:
	 *   - Registration eligibility checks
	 *   - Preventing duplicate active registrations
	 *
	 * Notes:
	 *   - Lock-free predicate
	 *   - Must be evaluated under an advisory transaction lock
	 *     when used in write paths to avoid race conditions
	 */
	SELECT EXISTS(
		SELECT 1
		FROM app.session_participation
		WHERE session_id = p_session_id
			AND user_id = p_user_id
			AND cancelled_at IS NULL
			AND (
				paid_at IS NOT NULL
				OR expires_at > now()
			)
	);
$$;

COMMENT ON FUNCTION app_fcn.has_active_participation(uuid, uuid) IS
'Returns true if the user already has an active (non-cancelled)
participation for the given session.';

create or replace function app_fcn.is_registration_open(
	p_session_id uuid
)
returns boolean
language sql
security definer
stable
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_registration_open
	 *
	 * Determines whether registration is currently allowed
	 * for a given session.
	 *
	 * A session is considered open for registration if:
	 *   - The session exists
	 *   - The session is not cancelled
	 *   - The current time is strictly before starts_at
	 *
	 * Notes:
	 *   - This function does not check capacity constraints
	 *     or existing participations.
	 *   - Intended to be composed with other predicates
	 *     (e.g. is_full, has_active_participation).
	 *
	 * Returns:
	 *   true  if registration is open
	 *   false otherwise
	 */
	SELECT now() < starts_at
	FROM app.sessions
	WHERE id = p_session_id
		AND cancelled_at IS NULL;
$$;

COMMENT ON FUNCTION app_fcn.is_registration_open(uuid) IS
'Returns true if the session exists, is not cancelled,
and registration is still open (before session start).';