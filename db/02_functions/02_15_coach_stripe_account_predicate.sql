CREATE OR REPLACE FUNCTION app_fcn.stripe_account_exists(
    p_coach_id uuid
)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.stripe_account_exists
 *
 * Checks whether a Stripe Connect account exists for the given coach.
 *
 * Authorization:
 *   - Caller must be a coach
 *
 * Behavior:
 *   - Returns TRUE if a Stripe account row exists for the coach
 *   - Returns FALSE otherwise
 *
 * Notes:
 *   - Read-only and transaction-stable
 *   - Used to enforce idempotent Stripe account creation
 *   - Safe to call under concurrent access
 */
BEGIN
    IF NOT app_fcn.is_coach() THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    RETURN EXISTS (
        SELECT 1
        FROM app.coach_stripe_accounts
        WHERE coach_id = p_coach_id
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.stripe_account_exists(uuid) IS
'Returns whether a Stripe Connect account exists for the given coach.
Performs coach-only authorization and is used to enforce idempotent
Stripe account creation flows.';
