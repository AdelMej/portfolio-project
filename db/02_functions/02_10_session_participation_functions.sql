CREATE OR REPLACE FUNCTION app_fcn.create_session_participation(
    p_user_id uuid,
    p_session_id uuid
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
        registered_at
    ) VALUES (
		gen_random_uuid(),
        p_session_id,
        p_user_id,
        now()
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.create_session_participation(uuid, uuid) IS
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
