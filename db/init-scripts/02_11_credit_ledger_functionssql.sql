\c app

CREATE OR REPLACE FUNCTION app_fcn.fetch_credit(
    p_user_id uuid,
    p_currency text
)
RETURNS integer
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
/*
 * app_fcn.fetch_credit_fcn
 *
 * Returns the current credit balance (in cents) for the given user.
 *
 * The balance is derived by summing all entries in the credit ledger
 * and represents the authoritative source of truth for user credit.
 *
 * Authorization:
 *   - A user may fetch their own credit balance
 *   - An admin may fetch any user's credit balance
 *
 * Notes:
 *   - The credit ledger is append-only
 *   - No state is mutated by this function
 *   - Safe for concurrent access and retries
 */
BEGIN
    IF NOT (app_fcn.is_self(p_user_id) OR app_fcn.is_admin()) THEN
        RAISE EXCEPTION 'permission denied'
            USING ERRCODE = 'AP401';
    END IF;

    RETURN (
        SELECT COALESCE(SUM(amount_cents), 0)
        FROM app.credit_ledger
        WHERE user_id = p_user_id
		AND currency = p_currency
    );
END;
$$;

COMMENT ON FUNCTION app_fcn.fetch_credit(uuid, text) IS
'Returns the current credit balance (in cents) for a user and currency
by summing all entries in the credit ledger.

The balance is derived, authoritative, and based on an append-only
ledger model.

Authorization:
- Users may fetch their own credit balance
- Admins may fetch any user credit balance.';

create or replace function app_fcn.create_credit_entry(
	p_user_id uuid,
	p_amount_cents int,
	p_currency text,
	p_cause text
)
returns void
language plpgsql
security definer
SET search_path = app, app_fcn, pg_temp
as $$
	/*
	 * create_credit_entry
	 *
	 * Appends a credit ledger entry for a user.
	 *
	 * This function enforces the following invariants:
	 * - Only the user themselves or an admin may create a credit entry.
	 * - The credit amount must be non-zero.
	 * - A user's credit balance must never become negative.
	 *
	 * Credit is modeled as an append-only ledger:
	 * - Positive amounts increase the user's balance.
	 * - Negative amounts decrease the user's balance.
	 *
	 * Concurrency safety:
	 * - Uses an advisory transaction lock scoped to the user to prevent
	 *   concurrent credit modifications and race conditions.
	 *
	 * Errors:
	 * - AP401: Permission denied.
	 * - AP400: Invalid amount (zero).
	 * - AB400: Credit balance would become negative.
	 */
	BEGIN
		perform pg_advisory_xact_lock(
			hashtext('user' || p_user_id::text)
		);
	
		IF NOT (app_fcn.is_self(p_user_id) or app_fcn.is_admin()) THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF p_amount_cents = 0 THEN
        	RAISE EXCEPTION 'amount cannot be zero'
            	USING ERRCODE = 'AP400';
    	END IF;

		IF app_fcn.fetch_credit(p_user_id, p_currency) + p_amount_cents < 0 THEN
			RAISE EXCEPTION 'credit cannot be negative'
				USING ERRCODE = 'AB400';
		END IF;

		INSERT INTO app.credit_ledger (
			id,
	        user_id,
	        amount_cents,
	        currency,
	        cause,
	        created_at
	    ) VALUES (
			gen_random_uuid(),
	        p_user_id,
	        p_amount_cents,
	        p_currency,
	        p_cause,
	        now()
	    );
	END;
$$;

COMMENT ON FUNCTION app_fcn.create_credit_entry(
    uuid,
    int,
    text,
    text
) IS
'Creates a credit ledger entry for a user.

The function enforces authorization, prevents zero-amount entries,
and ensures that the user''s credit balance never becomes negative.

Credit is represented as an append-only ledger where positive amounts
increase balance and negative amounts decrease balance.

An advisory transaction lock scoped to the user is used to prevent
concurrent credit modifications.';
