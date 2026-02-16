\c app

CREATE OR replace FUNCTION app_fcn.is_session_cancelled(
	p_session_id uuid
)
returns boolean
language sql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_cancelled
	 * --------------------
	 * Checks whether a session is cancelled.
	 *
	 * A session is considered cancelled if and only if:
	 *   - the session exists
	 *   - and `cancelled_at` is NOT NULL
	 *
	 * This is a derived state predicate:
	 *   - no flags
	 *   - no side effects
	 *   - safe to call repeatedly (idempotent)
	 *
	 * Returns:
	 *   TRUE  -> session exists and is cancelled
	 *   FALSE -> session does not exist or is not cancelled
	 *
	 * Notes:
	 *   - Implemented as an EXISTS query for efficiency
	 *   - SECURITY DEFINER is required as this function is used
	 *     inside other privileged domain functions
	 *   - search_path is explicitly set to prevent injection
	 */
	SELECT EXISTS (
		SELECT 1
		FROM app.sessions
		WHERE id = p_session_id
		AND cancelled_at is NOT NULL
	);
$$;

COMMENT ON FUNCTION app_fcn.is_session_cancelled(uuid) IS
'Predicate that returns TRUE if and only if the session exists and is cancelled (cancelled_at IS NOT NULL).
Side-effect free, idempotent, and safe to call repeatedly.
Used as a domain invariant guard inside cancellation and auditing logic.';

create or replace function app_fcn.session_exists(
	p_session_id uuid
)
returns boolean
language sql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.session_exists
	 * ----------------------
	 * Predicate function that determines whether a session exists.
	 *
	 * Behavior:
	 *   TRUE  -> session exists
	 *   FALSE -> session does not exist
	 *
	 * Properties:
	 *   - Side-effect free
	 *   - Idempotent
	 *   - Safe to call repeatedly (spam-safe)
	 *
	 * Intended usage:
	 *   - Guard conditions in domain SQL functions
	 *   - Early-return predicates
	 *   - Set-based logic (SELECT / WHERE / JOIN / EXISTS)
	 *
	 * Design notes:
	 *   - Implemented using EXISTS for optimal performance
	 *   - SECURITY DEFINER for use in privileged domain logic
	 *   - search_path fixed to prevent injection
	 */
	SELECT EXISTS(
		SELECT 1
		FROM app.sessions
		WHERE id = p_session_id
	);
$$;

COMMENT ON FUNCTION app_fcn.session_exists(uuid) IS
'Predicate that returns TRUE if the session exists, FALSE otherwise.
Side-effect free and idempotent.
Designed for guard conditions and set-based domain logic.';

create or replace function app_fcn.is_session_overlapping(
	p_starts_at timestamptz,
	p_ends_at timestamptz
)
returns boolean
language sql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_session_overlapping
	 *
	 * Returns true if the given time range [p_starts_at, p_ends_at)
	 * overlaps with any existing non-cancelled session.
	 *
	 * Used as a domain-level predicate to enforce the invariant:
	 *   - active sessions must not overlap in time
	 *
	 * Notes:
	 *   - Uses half-open ranges ([)) to allow back-to-back sessions
	 *   - Ignores cancelled sessions (cancelled_at IS NULL)
	 *   - Intended to be called inside transactional domain functions
	 */
	SELECT EXISTS (
		SELECT 1
		FROM app.sessions
		WHERE tstzrange(starts_at, ends_at, '[)')
			&& tstzrange(p_starts_at, p_ends_at, '[)')
			AND cancelled_at IS NULL
	);
$$;

COMMENT ON FUNCTION app_fcn.is_session_overlapping(
	timestamptz,
	timestamptz
) IS
'Checks whether a given [start, end) time interval overlaps with any existing non-cancelled session.
Used as a domain predicate to enforce the invariant that active sessions must not overlap.';

create or replace function app_fcn.is_session_owner(
	p_user_id uuid,
	p_session_id uuid
)
returns boolean
language sql
STABLE
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_session_owner
	 *
	 * Returns true if the given user is the coach/owner of the session
	 * and the session is not cancelled.
	 *
	 * Used as a domain-level predicate for authorization checks where
	 * only the owning coach is allowed to mutate session logistics
	 * (e.g. title or scheduling).
	 *
	 * Notes:
	 *   - Cancelled sessions are treated as non-ownable
	 *   - Pure predicate, no side effects
	 *   - Intended to be composed with higher-level domain functions
	 */
	SELECT EXISTS (
		SELECT 1
		FROM app.sessions
		WHERE id = p_session_id
			AND coach_id = p_user_id
			AND status != 'cancelled'
	);
$$;

COMMENT ON FUNCTION app_fcn.is_session_owner(
	uuid,
	uuid
) IS
'Predicate: returns true if the user is the owning coach of a non-cancelled session.';

create or replace function app_fcn.is_session_overlapping_except(
	p_starts_at timestamptz,
	p_ends_at timestamptz,
	p_excluded_session_id uuid
)
returns boolean
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.is_session_overlapping_except
	 *
	 * Returns true if the given time range [p_starts_at, p_ends_at)
	 * overlaps with any existing non-cancelled session,
	 * excluding the provided session id.
	 *
	 * Domain invariant:
	 *   - active sessions must not overlap in time
	 *
	 * Preconditions:
	 *   - p_excluded_session_id MUST NOT be NULL
	 *
	 * Notes:
	 *   - Uses half-open ranges ([)) to allow back-to-back sessions
	 *   - Cancelled sessions are ignored (cancelled_at IS NULL)
	 *   - Raises a domain exception if called with a NULL excluded id
	 *   - Intended for update flows inside transactional domain functions
	 */
	BEGIN
		IF p_excluded_session_id IS NULL THEN
			RAISE EXCEPTION 'p_excluded_session_id must not be NULL'
				USING ERRCODE = 'AP400';
		END IF;
	
		return EXISTS (
			SELECT 1
			FROM app.sessions
			WHERE id <> p_excluded_session_id
				AND tstzrange(starts_at, ends_at, '[)')
					&& tstzrange(p_starts_at, p_ends_at, '[)')
				AND cancelled_at IS NULL
		);
	END;
$$;

COMMENT ON FUNCTION app_fcn.is_session_overlapping_except(
	timestamptz,
	timestamptz,
	uuid
) IS
'Predicate: checks for overlapping active sessions, excluding the given session id. Raises if excluded id is NULL.';

CREATE OR replace FUNCTION app_fcn.is_session_cancelled(
	p_session_id uuid
)
returns boolean
language sql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * is_session_cancelled
	 * --------------------
	 * Checks whether a session has been cancelled.
	 *
	 * A session is considered cancelled if its `cancelled_at` column
	 * is non-NULL in the `app.sessions` table.
	 *
	 * This function is:
	 * - Read-only
	 * - Side-effect free
	 * - Safe to call multiple times
	 *
	 * Parameters:
	 *   p_session_id (uuid)
	 *     The unique identifier of the session to check.
	 *
	 * Returns:
	 *   boolean
	 *     TRUE  if the session exists and is cancelled
	 *     FALSE otherwise
	 *
	 * Notes:
	 * - Does not raise if the session does not exist
	 * - Intended for use in invariants, guards, and early-return checks
	 */
	SELECT EXISTS (
		SELECT 1
		FROM app.sessions
		WHERE id = p_session_id
			AND cancelled_at IS NOT NULL
	)
$$;

COMMENT ON FUNCTION app_fcn.is_session_cancelled(uuid)
IS 'Returns true if the given session has been cancelled (cancelled_at IS NOT NULL).';

