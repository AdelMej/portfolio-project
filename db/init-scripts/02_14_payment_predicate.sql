\c app

CREATE OR REPLACE FUNCTION app_fcn.is_already_paid(
    p_session_id uuid,
    p_user_id uuid
)
RETURNS boolean
LANGUAGE SQL
STABLE
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
    /*
     * app_fcn.is_already_paid
     *
     * Determines whether a successful payment has already been recorded
     * for a given session and user.
     *
     * Semantics:
     *   - Returns TRUE if a payment row exists
     *   - Returns FALSE otherwise
     *
     * Domain meaning:
     *   - A payment row represents a successful money transfer
     *   - Failed or pending payments are not stored
     *
     * Usage:
     *   - Enforces payout idempotency
     *   - Prevents double payouts for the same session
     *
     * Notes:
     *   - Read-only predicate
     *   - Assumes payments table contains only successful payments
     *   - Safe to use as a guard before initiating Stripe transfers
     */
    SELECT EXISTS(
        SELECT 1
        FROM app.payments
        WHERE user_id = p_user_id
          AND session_id = p_session_id
    );
$$;

COMMENT ON FUNCTION app_fcn.is_already_paid(uuid, uuid)
IS
'Checks whether a successful payment already exists for the given session and user. Used to enforce payout idempotency and prevent duplicate Stripe transfers.';
