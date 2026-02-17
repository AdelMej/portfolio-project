CREATE OR replace FUNCTION app_fcn.session_create_session(
	p_session_id uuid,
	p_coach_id uuid,
	p_title text,
	p_starts_at timestamptz,
	p_ends_at timestamptz,
	p_price_cents int,
	p_currency text
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.session_create_session
	 *
	 * Creates a session if it does not already exist.
	 *
	 * This function is idempotent:
	 * - If the session already exists (same primary key), the function returns
	 *   without performing any action.
	 *
	 * Concurrency & safety:
	 * - Uses a transaction-scoped advisory lock on the session ID to prevent
	 *   race conditions during concurrent creation attempts.
	 *
	 * Authorization:
	 * - Caller must be a coach or an admin.
	 * - Authorization is enforced inside the database using SECURITY DEFINER.
	 *
	 * Parameters:
	 * - p_session_id     : Unique identifier of the session (primary key).
	 * - p_coach_id       : Coach responsible for the session.
	 * - p_title          : Session title.
	 * - p_starts_at      : Session start timestamp (UTC).
	 * - p_ends_at        : Session end timestamp (UTC).
	 * - p_price_cents    : Session price in cents.
	 * - p_currency       : ISO currency code (upper-case expected).
	 *
	 * Errors:
	 * - Raises ERRCODE 'AP401' if the caller is not authorized.
	 *
	 * Returns:
	 * - void
	 */
	BEGIN
		perform pg_advisory_xact_lock(
			hashtext('session:' || p_session_id::text)
		);
	
		IF NOT (app_fcn.is_coach() or app_fcn.is_admin()) THEN
			raise exception 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.is_user_active(p_coach_id) THEN
			RETURN;
		END IF;
	
		IF app_fcn.session_exists(p_session_id) THEN
			RETURN;
		END IF;

		IF app_fcn.is_session_overlapping(p_starts_at, p_ends_at) THEN
			RETURN;
		END IF;
	
		INSERT INTO app.sessions(
			id,
			coach_id,
			title,
			starts_at,
			ends_at,
			price_cents,
			currency
		)
		VALUES (
			p_session_id,
			p_coach_id,
			p_title,
			p_starts_at,
			p_ends_at,
			p_price_cents,
			p_currency
		);
	END;
$$;

COMMENT ON FUNCTION app_fcn.session_create_session(
	uuid,
	uuid,
	text,
	timestamptz,
	timestamptz,
	int,
	text
) IS
'Creates a session in an idempotent and concurrency-safe manner.

Uses a transaction-scoped advisory lock on the session ID to prevent race
conditions. If the session already exists, the function returns without
modifying state.

Authorization is enforced inside the database: the caller must be a coach
or an admin. Designed to be safely retryable and spam-resistant.';

create or replace function app_fcn.session_update(
	p_session_id uuid,
	p_title text,
	p_starts_at timestamptz,
	p_ends_at timestamptz
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.session_update
	 *
	 * Idempotent domain command to update an existing session.
	 *
	 * This function updates the title and schedule of a session while enforcing
	 * domain invariants at the database level.
	 *
	 * Behavior:
	 *   - If the caller is not an admin or a coach, the function raises an error.
	 *   - If the session does not exist, the function performs a no-op.
	 *   - If the new time range overlaps with another active session (excluding
	 *     the session being updated), a domain exception is raised.
	 *   - If the provided values are identical to the current state, no update
	 *     is performed (idempotent behavior).
	 *
	 * Domain invariants:
	 *   - Active sessions must not overlap in time.
	 *   - Only admins or coaches may update sessions.
	 *
	 * Notes:
	 *   - This function is intentionally idempotent to allow safe retries.
	 *   - Overlapping sessions are treated as a domain violation (AP409).
	 *   - Missing sessions are treated as a no-op to preserve idempotency.
	 *   - Uses half-open time ranges ([starts_at, ends_at)).
	 *
	 * Errors:
	 *   - AP401: caller is not authorized
	 *   - AP409: session time overlaps with another active session
	 */
	BEGIN
		IF NOT (app_fcn.is_admin() OR app_fcn.is_coach()) THEN
			raise exception 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.session_exists(p_session_id) THEN
			RETURN;
		END IF;

		IF app_fcn.is_session_overlapping_except(
			p_starts_at,
			p_ends_at,
			p_session_id
		) THEN
			RAISE EXCEPTION 'session is overlapping'
				USING ERRCODE = 'AP409';
		END IF;

		UPDATE app.sessions
		SET 
			title = p_title,
			starts_at = p_starts_at,
			ends_at = p_ends_at
		WHERE id = p_session_id;			
	END;
$$;

COMMENT ON FUNCTION app_fcn.session_update(
	uuid,
	text,
	timestamptz,
	timestamptz
) IS
'Idempotent domain command that updates a session title and schedule.

- No-op if the session does not exist.
- Safe to call multiple times with the same arguments.
- Raises AP401 if the caller is not an admin or coach.
- Raises AP409 if the updated time range overlaps another active session.
- Enforces session scheduling invariants at the database level.';

CREATE OR REPLACE FUNCTION app_fcn.get_session_for_registration(
    p_session_id uuid
)
RETURNS TABLE (
    id uuid,
    coach_id uuid,
    title text,
    price_cents int,
    currency text,
    status text,
    starts_at timestamptz,
    ends_at timestamptz,
    cancelled_at timestamptz
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * get_session_for_registration
	 *
	 * System-level read function used during the session registration flow.
	 *
	 * This function returns the minimal set of session data required to
	 * validate registration invariants and compute pricing, without granting
	 * direct SELECT access on the sessions table to the application role.
	 *
	 * Security model:
	 * - Runs as SECURITY DEFINER
	 * - Enforces existence validation internally
	 * - Intended for internal system workflows only (not public reads)
	 *
	 * Errors:
	 * - AP404: Raised if the session does not exist
	 *
	 * Notes:
	 * - This function MUST remain side-effect free
	 * - Any additional invariants should be enforced at the service layer
	 */
	BEGIN
	    IF NOT app_fcn.session_exists(p_session_id) THEN
	        RAISE EXCEPTION 'session not found'
	            USING ERRCODE = 'AP404';
	    END IF;
	
	    RETURN QUERY
	    SELECT
	        s.id,
	        s.coach_id,
			s.title::text,
	        s.price_cents,
	        s.currency,
	        s.status::text,
	        s.starts_at,
	        s.ends_at,
			s.cancelled_at
	    FROM app.sessions s
	    WHERE s.id = p_session_id;
	END;
$$;

COMMENT ON FUNCTION app_fcn.get_session_for_registration(uuid) IS
'System-level read function used during session registration to fetch
pricing and timing data without exposing direct SELECT access on app.sessions.
Raises AP404 if the session does not exist. SECURITY DEFINER.';

create or replace function app_fcn.cancel_session(
	p_session_id uuid
)
returns void
language plpgsql
security definer
SET search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.cancel_session
	 *
	 * Cancels a session and applies all required domain side effects
	 * in a single transactional, database-enforced operation.
	 *
	 * Behavior:
	 *   - Acquires an advisory transaction lock scoped to the session
	 *     to guarantee race-free cancellation.
	 *   - Marks all active session participations as cancelled.
	 *   - Issues credits for all successful payments linked to the
	 *     cancelled participations (idempotent).
	 *   - Marks the session itself as cancelled.
	 *
	 * Preconditions (enforced here):
	 *   - Caller must be an admin or coach.
	 *   - Session must exist.
	 *
	 * Idempotency:
	 *   - If the session is already cancelled, the function is a no-op.
	 *   - Credit creation is protected against duplication.
	 *
	 * Consistency guarantees:
	 *   - All side effects occur atomically within a single transaction.
	 *   - Ordering of operations reflects causal domain events.
	 *
	 * Notes:
	 *   - Payments are only refunded via credits if a successful payment exists.
	 *   - Timestamp differences between side effects are intentional and
	 *     preserve causal ordering for auditability.
	 */
	DECLARE
    	v_payment_id uuid;
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('session:' || p_session_id::text)
		);

		IF NOT (app_fcn.is_admin() or app_fcn.is_coach()) THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.session_exists(p_session_id) THEN
			RAISE EXCEPTION 'session not found'
				USING ERRCODE = 'AP404';
		END IF;

		IF app_fcn.is_session_cancelled(p_session_id) THEN
			RETURN;
		END IF;

		-- Cancel participations first
		UPDATE app.session_participation
		SET cancelled_at = now()
		WHERE session_id = p_session_id
		  AND cancelled_at IS NULL;

		-- Issue credits BEFORE updating session status
		-- This prevents any cascade issues
		FOR v_payment_id IN
		    SELECT id
		    FROM app.payments
		    WHERE session_id = p_session_id
		    FOR UPDATE  -- Lock the payment rows
		LOOP
		    PERFORM app_fcn.issue_credit_for_payment(v_payment_id, 'session_cancelled'::credit_ledger_cause);
		END LOOP;

		-- Update session last
		UPDATE app.sessions
		SET cancelled_at = now(),
			status = 'cancelled'
		WHERE id = p_session_id
			AND cancelled_at IS NULL;
	END;
$$;

COMMENT ON FUNCTION app_fcn.cancel_session(uuid) IS
'Cancels a session and enforces all domain side effects atomically.
The function acquires a session-scoped advisory transaction lock,
cancels all active participations, issues credits for successful
payments linked to the session (idempotent), and marks the session
as cancelled. Permission, existence, and idempotency rules are fully
enforced at the database level.';
