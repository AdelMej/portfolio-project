create or replace function app_fcn.create_payment(
	p_session_id uuid,
	p_user_id uuid,
	p_provider text,
	p_provider_payment_id text,
	p_gross_amount_cents int,
	p_provider_fee_cents int,
	p_net_amount_cents int,
	p_currency text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * create_payment
	 * --------------
	 * Creates a finalized payment record after a successful provider confirmation.
	 *
	 * This function is intended to be called from payment webhooks
	 * (e.g. Stripe payment_intent.succeeded).
	 *
	 * Behavior:
	 * - Acquires an advisory transaction lock on provider_payment_id
	 * - No-ops if a payment with the same provider_payment_id already exists
	 * - Inserts a new payment row otherwise
	 *
	 * Invariants:
	 * - Payments are immutable once created
	 * - Each provider_payment_id can only produce one payment
	 *
	 * Notes:
	 * - This function never raises exceptions
	 * - Fully idempotent and safe for concurrent webhook delivery
	 */
	BEGIN
	    -- Ensure idempotency across concurrent webhooks
	    PERFORM pg_advisory_xact_lock(
	        hashtext('payment:' || p_provider_payment_id)
	    );
	
	    -- Payment already exists → no-op
	    IF EXISTS (
	        SELECT 1
	        FROM app.payments
	        WHERE provider_payment_id = p_provider_payment_id
	    ) THEN
	        RETURN;
	    END IF;
	
	    INSERT INTO app.payments (
	        id,
	        session_id,
	        user_id,
	        provider,
	        provider_payment_id,
	        gross_amount_cents,
			provider_fee_cents,
			net_amount_cents,
	        currency,
	        created_at
	    ) VALUES (
	        gen_random_uuid(),
	        p_session_id,
	        p_user_id,
	        p_provider,
	        p_provider_payment_id,
	        p_gross_amount_cents,
			p_provider_fee_cents,
			p_net_amount_cents,
	        p_currency,
	        now()
	    );
	END;
$$;

COMMENT ON FUNCTION app_fcn.create_payment(
    uuid,
    uuid,
    text,
    text,
    integer,
    integer,
    integer,
    text
)
IS
'Creates a finalized payment record in an idempotent and race-safe manner.
Intended for payment provider webhooks. No-ops if the payment already exists.';

CREATE OR REPLACE FUNCTION app_fcn.get_payment_for_session(
    p_session_id uuid
)
RETURNS TABLE (
    amount_cents int,
    currency text
)
LANGUAGE SQL
STABLE
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
    /*
     * app_fcn.get_payment_for_session
     *
     * Computes the total net amount collected for a session and
     * returns it together with the session currency.
     *
     * Invariants:
     *   - Session currency is authoritative
     *   - All payments for a session are expected to use this currency
     *
     * Behavior:
     *   - Returns exactly one row if the session exists
     *   - Amount is zero when no payments are present
     *
     * Usage:
     *   - Coach payout calculation
     *
     * Notes:
     *   - Currency is sourced from sessions, not inferred from payments
     *   - Safe against empty payment sets
     */
    SELECT
        COALESCE(SUM(p.net_amount_cents), 0)::int AS amount_cents,
        s.currency
    FROM app.sessions s
    LEFT JOIN app.payments p
        ON p.session_id = s.id
    WHERE s.id = p_session_id
    GROUP BY s.currency;
$$;

COMMENT ON FUNCTION app_fcn.get_payment_for_session(uuid)
IS
'Aggregates the total net amount collected for a session and returns it with the session currency. Currency is sourced from the session as the authoritative value.';
