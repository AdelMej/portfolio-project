CREATE OR REPLACE FUNCTION app_fcn.create_payment_intent(
    p_user_id uuid,
    p_session_id uuid,
    p_provider text,
    p_provider_intent_id text,
    p_status text,
    p_amount_cents integer,
    p_credit_applied_cents integer,
    p_currency text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.create_payment_intent
 *
 * Persists a new payment intent associated with a session registration.
 *
 * This function records the payment intent metadata returned by the payment
 * provider (e.g. Stripe) and ensures idempotency at the database level.
 *
 * The function does NOT interact with the payment provider directly and does
 * NOT perform any payment state transitions. It only persists the intent as
 * reported by the provider at creation time.
 *
 * Authorization:
 *   - A user may only create a payment intent for themselves.
 *
 * Invariants:
 *   - A session must exist.
 *   - Only one active payment intent may exist per user and session.
 *   - Payment intents with status 'canceled' or 'failed' are ignored for
 *     idempotency checks.
 *
 * Errors:
 *   - AP401: permission denied
 *   - AP404: session not found
 *   - AP409: payment intent already exists
 */
BEGIN
    IF NOT app_fcn.is_self(p_user_id) THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    IF NOT app_fcn.session_exists(p_session_id) THEN
        RAISE EXCEPTION 'session not found'
            USING ERRCODE = 'AP404';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM app.payment_intents
        WHERE session_id = p_session_id
          AND user_id = p_user_id
          AND status NOT IN ('canceled', 'failed')
    ) THEN
        RAISE EXCEPTION 'payment intent already exists'
            USING ERRCODE = 'AP409';
    END IF;

    INSERT INTO app.payment_intents (
		id,
        user_id,
        session_id,
        provider,
        provider_intent_id,
        status,
        amount_cents,
        credit_applied_cents,
        currency,
        created_at
    ) VALUES (
		gen_random_uuid(),
        p_user_id,
        p_session_id,
        p_provider,
        p_provider_intent_id,
        p_status,
        p_amount_cents,
        p_credit_applied_cents,
        p_currency,
        now()
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.create_payment_intent(
    uuid,
    uuid,
    text,
    text,
    text,
    integer,
    integer,
    text
) IS
'Persists a new payment intent for a session registration.

This function records payment intent metadata returned by the payment
provider and enforces idempotency at the database level.

The function does not communicate with the payment provider and does not
manage payment state transitions.

Authorization:
- A user may only create a payment intent for themselves.

Errors:
- AP401: permission denied
- AP404: session not found
- AP409: payment intent already exists';

create or replace function app_fcn.get_by_identity(
	p_user_id uuid,
	p_session_id uuid,
	p_provider text
)
returns table (
	id uuid,
	user_id uuid,
	session_id uuid,
	provider text,
	provider_intent_id text,
	status text,
	credit_applied_cents int,
	amount_cents int,
	currency text
)
language sql
security definer
stable
set search_path = app, app_fcn, pg_temp
as $$
    /*
     * Fetch a payment intent by its provider identifier.
     *
     * This function is primarily used by webhook handlers (e.g. Stripe)
     * to resolve internal payment intent state from an external provider
     * event.
     *
     * The function does not perform permission checks by design:
     * it is intended to be called from trusted backend or system
     * contexts (SECURITY DEFINER).
     *
     * Parameters:
     *   p_provider_payment_id - Provider-side payment intent identifier
     *
     * Returns:
     *   A single row representing the payment intent if it exists,
     *   otherwise an empty result set.
     */
    SELECT
        pi.id,
        pi.user_id,
        pi.session_id,
        pi.provider,
        pi.provider_intent_id,
        pi.status,
        pi.credit_applied_cents,
        pi.amount_cents,
        pi.currency
    FROM app.payment_intents pi
    WHERE pi.user_id = p_user_id
		AND pi.session_id = p_session_id
		AND pi.provider = p_provider;
$$;

COMMENT ON FUNCTION app_fcn.get_by_identity(uuid, uuid, text)
IS
'Resolves an internal payment intent using a provider-side payment intent ID.
Used by payment webhooks to map external events to internal payment state.';

create or replace function app_fcn.mark_payment_intent(
	p_provider_payment_id text,
	p_provider_status text
)
returns void
language plpgsql
security definer
SET search_path = app, app_fcn, pg_temp
as $$
	/*
	 * mark_payment_intent
	 * -------------------
	 * Updates the status of a payment intent identified by its provider ID.
	 *
	 * This function is designed to be called from payment provider webhooks
	 * (e.g. Stripe) and is therefore:
	 *
	 * - Idempotent:
	 *   If the payment intent already has the given status, the function
	 *   performs a no-op and returns immediately.
	 *
	 * - Race-safe:
	 *   Uses an advisory transaction lock scoped to the provider payment ID
	 *   to prevent concurrent webhook deliveries from causing conflicting
	 *   updates.
	 *
	 * - Tolerant to out-of-order events:
	 *   If the payment intent does not yet exist in the database (e.g. webhook
	 *   arrives before intent persistence), the function performs a no-op.
	 *
	 * No exceptions are raised intentionally, as webhook delivery must not
	 * fail due to transient or duplicate events.
	 *
	 * Parameters:
	 *   p_provider_payment_id - Unique payment identifier from the provider
	 *   p_provider_status     - New status reported by the provider
	 *
	 * Returns:
	 *   void
	 */
	DECLARE
    	v_current_status text;
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('payment_intent' || p_provider_payment_id)
		);

		SELECT status
		INTO v_current_status
		FROM app.payment_intents
		WHERE provider_intent_id = p_provider_payment_id;
		
		-- Webhook may arrive before intent is persisted → no-op
		IF v_current_status IS NULL THEN
		    RETURN;
		END IF;
		
		-- Idempotency guard
		IF v_current_status = p_provider_status THEN
		    RETURN;
		END IF;
		
		UPDATE app.payment_intents
		SET status = p_provider_status
	    WHERE provider_intent_id = p_provider_payment_id;
	END;
$$;

COMMENT ON FUNCTION app_fcn.mark_payment_intent(text, text)
IS
'Updates the status of a payment intent based on provider webhook events.
The function is idempotent, race-safe via advisory locking, and tolerant to
out-of-order or duplicate webhook deliveries. Intended for internal system
use and never raises errors for missing or already-processed intents.';

CREATE OR REPLACE FUNCTION app_fcn.mark_participation_paid(
    p_session_id uuid,
    p_user_id uuid
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * mark_participation_paid
	 * -----------------------
	 * Marks a session participation as paid.
	 *
	 * This function is designed to be called from payment webhooks (e.g. Stripe)
	 * and is fully idempotent and race-safe.
	 *
	 * Behavior:
	 * - Acquires an advisory transaction lock on (session_id, user_id)
	 * - No-ops if the participation does not exist
	 * - No-ops if the participation is already paid
	 * - No-ops if the participation has been cancelled
	 * - Sets paid_at to now() otherwise
	 *
	 * Notes:
	 * - This function never raises exceptions
	 * - Safe to call multiple times or concurrently
	 * - Payment invariants are enforced at the database level
	 */
	DECLARE
	    v_paid_at timestamptz;
	    v_cancelled_at timestamptz;
		v_expires_at timestamptz;
	BEGIN
	    PERFORM pg_advisory_xact_lock(
	        hashtext('participation:' || p_session_id::text || ':' || p_user_id::text)
	    );
	
	    SELECT paid_at, cancelled_at, expires_at
	    INTO v_paid_at, v_cancelled_at, v_expires_at
	    FROM app.session_participation
	    WHERE session_id = p_session_id
	      AND user_id = p_user_id;
	
	    -- Participation does not exist → no-op (webhook-safe)
	    IF v_paid_at IS NULL AND v_cancelled_at IS NULL THEN
	        NULL;
	    END IF;
	
	    -- Already cancelled → no-op
	    IF v_cancelled_at IS NOT NULL THEN
	        RETURN;
	    END IF;
	
	    -- Already paid → idempotent
	    IF v_paid_at IS NOT NULL THEN
	        RETURN;
	    END IF;
	    
	    -- Expired
	    IF v_expires_at < now() THEN
	    	RETURN;
	    END IF;

	    UPDATE app.session_participation
	    SET paid_at = now()
	    WHERE session_id = p_session_id
	      AND user_id = p_user_id;
	END;
$$;

COMMENT ON FUNCTION app_fcn.mark_participation_paid(uuid, uuid)
IS
'Marks a session participation as paid in an idempotent and race-safe manner.
Intended for payment webhooks. No-ops if participation is missing, already paid,
or cancelled.';


CREATE OR REPLACE FUNCTION app_fcn.cancel_unpaid_participation(
    p_session_id uuid,
    p_user_id uuid
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * cancel_unpaid_participation
	 * ---------------------------
	 * Cancels a session participation that has not been paid.
	 *
	 * This function is intended for payment failure or cancellation events
	 * (e.g. Stripe payment_failed or canceled webhooks).
	 *
	 * Behavior:
	 * - Acquires an advisory transaction lock on (session_id, user_id)
	 * - No-ops if the participation does not exist
	 * - No-ops if the participation is already cancelled
	 * - No-ops if the participation has already been paid
	 * - Sets cancelled_at to now() otherwise
	 *
	 * Notes:
	 * - This function never raises exceptions
	 * - Fully idempotent and safe for concurrent webhook delivery
	 * - Ensures paid participations are never cancelled
	 */
	DECLARE
	    v_paid_at timestamptz;
	    v_cancelled_at timestamptz;
	BEGIN
	    PERFORM pg_advisory_xact_lock(
	        hashtext('participation:' || p_session_id::text || ':' || p_user_id::text)
	    );
	
	    SELECT paid_at, cancelled_at
	    INTO v_paid_at, v_cancelled_at
	    FROM app.session_participation
	    WHERE session_id = p_session_id
	      AND user_id = p_user_id;
	
	    -- Participation missing → no-op
	    IF v_paid_at IS NULL AND v_cancelled_at IS NULL THEN
	        NULL;
	    END IF;
	
	    -- Already cancelled → idempotent
	    IF v_cancelled_at IS NOT NULL THEN
	        RETURN;
	    END IF;
	
	    -- Paid → never cancel
	    IF v_paid_at IS NOT NULL THEN
	        RETURN;
	    END IF;
	
	    UPDATE app.session_participation
	    SET cancelled_at = now()
	    WHERE session_id = p_session_id
	      AND user_id = p_user_id;
	END;
$$;

COMMENT ON FUNCTION app_fcn.cancel_unpaid_participation(uuid, uuid)
IS
'Cancels an unpaid session participation in an idempotent and race-safe manner.
Used for payment failure or cancellation webhooks. No-ops if participation is
missing, already cancelled, or already paid.';

CREATE OR replace function app_fcn.set_provider_id(
	p_user_id uuid,
	p_session_id uuid,
	p_provider text,
	p_provider_intent_id text
)
returns void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * set_provider_id
	 *
	 * Associates a provider-specific payment intent identifier with an existing
	 * payment_intent row.
	 *
	 * Concurrency:
	 *   Uses pg_advisory_xact_lock scoped to (user_id, session_id) to ensure
	 *   that concurrent updates for the same logical payment intent are serialized.
	 *
	 * Behavior:
	 *   - Verifies the intent exists using app_fcn.intent_exists(...)
	 *   - Raises AP404 if no matching intent is found
	 *   - Updates provider_intent_id for the matching (user, session, provider)
	 *
	 * Security:
	 *   - SECURITY DEFINER
	 *   - search_path restricted to app, app_fcn, pg_temp
	 *
	 * Notes:
	 *   - Designed to be idempotent at the application level
	 *   - Does not create intents; only updates existing rows
	 */
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('user:' || p_user_id::text || ':session:' || p_session_id::text)
		);

		IF NOT app_fcn.intent_exists(p_user_id, p_session_id, p_provider) THEN
			RAISE EXCEPTION 'payment intent not found'
				USING ERRCODE = 'AP404';
		END IF;

		UPDATE app.payment_intents
		SET
			provider_intent_id = p_provider_intent_id
		WHERE user_id = p_user_id
			AND session_id = p_session_id
			AND provider = p_provider;
	END;
$$;

COMMENT ON FUNCTION app_fcn.set_provider_id(uuid, uuid, text, text)
IS
'Associates a provider-specific payment intent identifier with an existing payment_intent row.

Concurrency-safe via pg_advisory_xact_lock scoped to (user_id, session_id).
Raises AP404 if the intent does not exist.
Does not create rows; only updates provider_intent_id.';
