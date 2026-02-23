CREATE OR REPLACE FUNCTION app_fcn.stripe_account_is_valid(
    p_coach_id uuid
)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
STABLE
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * app_fcn.stripe_account_is_valid
	 *
	 * Determines whether a coach has a fully operational Stripe Connect account.
	 *
	 * A Stripe account is considered valid when:
	 *   - details_submitted = TRUE
	 *   - charges_enabled  = TRUE
	 *   - payouts_enabled  = TRUE
	 *
	 * Authorization:
	 *   - Caller must be a coach
	 *
	 * Usage:
	 *   - Session creation eligibility
	 *   - Payment initiation guards
	 *   - Payout enforcement
	 *
	 * Notes:
	 *   - Stripe is the source of truth for account state
	 *   - Read-only and transaction-stable
	 */
	
	SELECT EXISTS (
	    SELECT 1
	    FROM app.coach_stripe_accounts
	    WHERE coach_id = p_coach_id
	    AND details_submitted = TRUE
	    AND charges_enabled = TRUE
		AND payouts_enabled = True
	);
$$;

COMMENT ON FUNCTION app_fcn.stripe_account_is_valid(uuid) IS
'Returns whether a Stripe Connect account exists for the given coach.
Performs coach-only authorization and is used to enforce idempotent
Stripe account creation flows.';

CREATE OR replace FUNCTION app_fcn.stripe_account_exists(
	p_coach_id uuid
)
RETURNS boolean
LANGUAGE SQL
stable
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * Checks whether a Stripe account is registered for the given coach.
	 *
	 * This function returns true if a Stripe account exists for the provided
	 * coach identifier, and false otherwise.
	 *
	 * It is intended to be used as a lightweight predicate in business logic
	 * to validate Stripe-related operations (payouts, credits, etc.) without
	 * exposing Stripe account details.
	 */
	SELECT EXISTS(
		SELECT 1
		FROM app.coach_stripe_accounts
		WHERE coach_id = p_coach_id
	);
$$;

COMMENT ON FUNCTION app_fcn.stripe_account_exists(uuid)
IS 'Returns true if a Stripe account exists for the given coach ID; used as a lightweight predicate for validating Stripe-related operations.';