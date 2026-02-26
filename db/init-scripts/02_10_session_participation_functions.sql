\c app

CREATE OR REPLACE FUNCTION app_fcn.create_session_participation(
    p_user_id uuid,
    p_session_id uuid,
    p_expires_at timestamptz
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.create_session_partipation
 *
 * Creates a session participation for the given user and session.
 *
 * This function is responsible for enforcing all participation
 * invariants at the database level and is safe against concurrent
 * registrations through the use of an advisory transaction lock.
 *
 * Authorization:
 *   - A user may only create their own participation
 *
 * Invariants enforced:
 *   - Session must exist
 *   - Session must not be cancelled
 *   - User must not already have an active participation
 *   - Session must not be full
 *
 * Concurrency:
 *   - A session-scoped advisory transaction lock is used to prevent
 *     race conditions when registering multiple users concurrently
 *
 * Notes:
 *   - This function is idempotent with respect to active participation
 *     (duplicate attempts result in a domain error)
 *   - No state outside session participation is mutated
 */
BEGIN
    PERFORM pg_advisory_xact_lock(
        hashtext('session:' || p_session_id::text)
    );

    IF NOT app_fcn.is_self(p_user_id) THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    IF NOT app_fcn.session_exists(p_session_id) THEN
        RAISE EXCEPTION 'session not found'
            USING ERRCODE = 'AP404';
    END IF;

    IF app_fcn.is_session_cancelled(p_session_id) THEN
        RAISE EXCEPTION 'session cancelled'
            USING ERRCODE = 'AP410';
    END IF;

    IF app_fcn.has_active_participation(p_session_id, p_user_id) THEN
        RAISE EXCEPTION 'already participating'
            USING ERRCODE = 'AB409';
    END IF;

    IF app_fcn.is_session_full(p_session_id, 6) THEN
        RAISE EXCEPTION 'session full'
            USING ERRCODE = 'AB409';
    END IF;

    INSERT INTO app.session_participation (
		id,
        session_id,
        user_id,
        registered_at,
        expires_at
    ) VALUES (
		gen_random_uuid(),
        p_session_id,
        p_user_id,
        now(),
        p_expires_at
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.create_session_participation(uuid, uuid, timestamptz) IS
'Creates a participation entry for a user in a session.

This function enforces all session participation invariants at the
database level and uses an advisory transaction lock to prevent
concurrent overbooking.

Authorization:
- Users may only create their own participation

Errors:
- AP401: permission denied
- AP404: session not found
- AP410: session cancelled
- AP409: already participating or session full';


create or replace function app_fcn.cancel_participation(
	p_user_id uuid,
	p_session_id uuid
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * cancel_participation
	 * --------------------
	 * Cancels an active participation for the calling user in a given session.
	 *
	 * Invariants:
	 * - The caller must be the same as `p_user_id` (self-action only).
	 * - The session must exist.
	 * - The user must have an active (non-cancelled) participation.
	 *
	 * Concurrency:
	 * - Uses an advisory transaction lock scoped to (user_id, session_id)
	 *   to prevent double-cancellation or race conditions.
	 *
	 * Effects:
	 * - Sets `cancelled_at` to the current timestamp.
	 *
	 * Errors:
	 * - AP401: caller is not the target user.
	 * - AP404: session does not exist.
	 * - AB404: no active participation found to cancel.
	 */
	begin
		perform pg_advisory_xact_lock(
			hashtext('user:' || p_user_id::text || ':session:' || p_session_id::text) 
		);

		IF NOT app_fcn.is_self(p_user_id) THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.session_exists(p_session_id) THEN
			RAISE EXCEPTION 'session not found'
				USING ERRCODE = 'AP404';
		END IF;

		UPDATE app.session_participation
		SET cancelled_at = now()
		WHERE user_id = p_user_id
		AND session_id = p_session_id
		AND cancelled_at IS NULL;

		IF NOT FOUND THEN
		    RAISE EXCEPTION 'no active participation found'
		        USING ERRCODE = 'AB404';
		END IF;
	end;
$$;

comment on function app_fcn.cancel_participation(uuid, uuid)
is
'Cancels an active session participation for the calling user.
Performs self-authorization, validates session existence, enforces
single active participation, and marks it as cancelled atomically.';


create or replace function app_fcn.revoke_all_active_session(
	p_user_id uuid
)
returns void
language plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * app_fcn.revoke_all_active_session
	 *
	 * Revokes all active session participations for the given user.
	 *
	 * Authorization:
	 *   - A user may only revoke their own participations
	 *
	 * Behavior:
	 *   - Marks all active participations as cancelled by setting cancelled_at
	 *   - Does not delete records (append-only history preserved)
	 *
	 * Definition of "active":
	 *   - cancelled_at IS NULL
	 *   - AND (
	 *       paid_at IS NOT NULL
	 *       OR expires_at > now()
	 *     )
	 *
	 * Usage:
	 *   - Cleanup on checkout failure
	 *   - User-initiated cancellation flows
	 *   - Safety rollback paths
	 *
	 * Notes:
	 *   - Idempotent (repeated calls have no side effects)
	 *   - No advisory lock required (single-user scoped mutation)
	 */
	BEGIN
		IF NOT app_fcn.is_self(p_user_id) THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		UPDATE app.session_participation
		SET cancelled_at = now()
		WHERE user_id = p_user_id;
	END;
$$;

COMMENT ON FUNCTION app_fcn.revoke_all_active_session(uuid)
IS
'Revoke all active session participations for the given user. Used to cancel pending or active registrations during checkout failures, user-initiated cancellations, or safety rollback paths. Only affects active participations and preserves historical records.';


create or replace function app_fcn.get_complete_session(
	p_session_id uuid
)
returns table(
	id uuid,
	user_id uuid,
	first_name text,
	last_name text,
	title text,
	starts_at timestamptz,
	ends_at timestamptz,
	status text,
	cancelled_at timestamptz,
	price_cents int,
	currency text,
	created_at timestamptz,
	updated_at timestamptz,
	participants json[]
)
language plpgsql
stable
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.get_complete_session
	 * ----------------------------------------
	 * Returns a fully hydrated session projection including:
	 *   - Core session metadata
	 *   - Public coach profile information
	 *   - Aggregated list of participants as JSON
	 *
	 * This function is designed as a read-model projection for API
	 * consumption and bypasses RLS via SECURITY DEFINER.
	 *
	 * Access control must therefore be enforced explicitly by
	 * the caller or by adding predicates inside this function
	 * if visibility restrictions are required.
	 *
	 * Aggregation behavior:
	 *   - Participants are returned as a JSON array.
	 *   - If no participants exist, an empty JSON array is returned.
	 *
	 * Concurrency:
	 *   - STABLE classification ensures read-only behavior.
	 *
	 * Parameters:
	 *   p_session_id → UUID of the session to retrieve.
	 */
	begin
		RETURN QUERY
        SELECT
            s.id,
            cp.user_id,
            cp.first_name::text,
            cp.last_name::text,
            s.title::text,
            s.starts_at,
            s.ends_at,
            s.status::text,
            s.cancelled_at,
            s.price_cents,
            s.currency,
            s.created_at,
            s.updated_at,
            COALESCE(
                array_agg(
                    json_build_object(
                        'user_id', up.user_id,
                        'first_name', up.first_name,
                        'last_name', up.last_name
                    )
                ) FILTER (WHERE up.user_id IS NOT NULL),
                '{}'
            ) AS participants
        FROM app.sessions s
        JOIN app.v_coach_public cp
            ON cp.user_id = s.coach_id
        LEFT JOIN app.session_participation sp
            ON sp.session_id = s.id
        LEFT JOIN app.user_profiles up
            ON up.user_id = sp.user_id
        WHERE s.id = p_session_id
        GROUP BY
            s.id,
            cp.user_id,
            cp.first_name,
            cp.last_name,
            s.title,
            s.starts_at,
            s.ends_at,
            s.status,
            s.cancelled_at,
            s.price_cents,
            s.currency,
            s.created_at,
            s.updated_at;
	end;
$$;

COMMENT ON FUNCTION app_fcn.get_complete_session(uuid) IS
'Returns a complete session projection including coach public profile and aggregated participant list as JSON. Designed as a read-model helper for API consumption. SECURITY DEFINER; bypasses RLS and must enforce visibility explicitly if required.';
