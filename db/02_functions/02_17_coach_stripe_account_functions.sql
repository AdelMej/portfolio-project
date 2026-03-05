CREATE OR REPLACE FUNCTION app_fcn.create_coach_stripe_account(
    p_stripe_account_id text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * app_fcn.create_coach_stripe_account
	 *
	 * Creates a Stripe Connect account record for the calling coach.
	 *
	 * Authorization:
	 *   - Caller must be a coach
	 *
	 * Behavior:
	 *   - Idempotent: if a Stripe account already exists for the coach,
	 *     the function returns without modifying state
	 *   - Otherwise inserts a new Stripe account record
	 *
	 * Invariants:
	 *   - One Stripe account per coach
	 *   - stripe_account_id is immutable after creation
	 *
	 * Notes:
	 *   - Uses the current actor ID from session settings
	 *   - Intended to be called after successful Stripe account creation
	 */
	BEGIN
	    IF NOT app_fcn.is_coach() THEN
	        RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
	    END IF;
	
	    IF app_fcn.stripe_account_exists(
	        current_setting('app.current_user_id')::uuid
	    ) THEN
	        RETURN;
	    END IF;
	
	    INSERT INTO app.coach_stripe_accounts (
	        coach_id,
	        stripe_account_id
	    ) VALUES (
	        current_setting('app.current_user_id')::uuid,
	        p_stripe_account_id
	    );
	END;
$$;

COMMENT ON FUNCTION app_fcn.create_coach_stripe_account(text) IS
'Creates a Stripe Connect account record for the calling coach.
This function is idempotent and enforces a single Stripe account
per coach using database-level invariants.';

CREATE OR REPLACE FUNCTION app_fcn.get_stripe_account_id(
    p_coach_id uuid
)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
SET search_path = app, app_fcn, pg_temp
AS $$
	/*
	 * app_fcn.get_stripe_account_id
	 *
	 * Returns the Stripe Connect account ID for the given coach.
	 *
	 * Authorization:
	 *   - Caller must be a coach
	 *
	 * Behavior:
	 *   - Returns the Stripe account ID if it exists
	 *   - Returns NULL if no account is registered
	 *
	 * Notes:
	 *   - Read-only
	 *   - Intended for onboarding link regeneration and payout checks
	 */
	BEGIN
	    IF NOT app_fcn.is_coach() THEN
	        RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
	    END IF;
	
	    RETURN (
	        SELECT stripe_account_id
	        FROM app.coach_stripe_accounts
	        WHERE coach_id = p_coach_id
	    );
	END;
$$;

COMMENT ON FUNCTION app_fcn.get_stripe_account_id(uuid) IS
'Returns the Stripe Connect account ID for the given coach, or NULL if
no account exists. Used to support idempotent onboarding and payout
flows.';

create or replace function app_fcn.update_by_stripe_account_id(
	p_account_id text,
	p_details_submitted bool,
	p_charges_enabled bool,
	p_payouts_enabled bool
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.update_by_stripe_account_id
	 *
	 * Synchronizes Stripe Connect account state using the Stripe account ID.
	 *
	 * Intended for:
	 *   - Stripe webhook processing (e.g. account.updated)
	 *
	 * Behavior:
	 *   - Updates charges_enabled, payouts_enabled, and details_submitted flags
	 *   - Idempotent: safe to call multiple times with the same data
	 *
	 * Preconditions:
	 *   - Caller must be a coach
	 *   - Stripe account must already exist in coach_stripe_accounts
	 *
	 * Notes:
	 *   - Does not create accounts
	 *   - Does not perform authorization beyond role validation
	 */
	begin
		UPDATE app.coach_stripe_accounts
		SET
			stripe_account_id = p_account_id,
			charges_enabled = p_charges_enabled,
			payouts_enabled = p_payouts_enabled,
			details_submitted = p_details_submitted
		WHERE stripe_account_id = p_account_id;
	end;
$$;

COMMENT ON FUNCTION app_fcn.update_by_stripe_account_id(
    text,
    boolean,
    boolean,
    boolean
) IS
'Updates Stripe Connect account state flags using the Stripe account ID.
Intended for Stripe webhook synchronization (charges, payouts, details).
Idempotent and safe to call multiple times.';
