\c app

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