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

CREATE OR REPLACE FUNCTION app_fcn.issue_credit_for_payment(
    p_payment_id uuid,
    p_cause app.credit_ledger_cause
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
/*
 * app_fcn.issue_credit_for_payment
 *
 * Issues a credit ledger entry for a given payment, if and only if
 * such a credit has not already been issued for the same cause.
 *
 * This function is designed to be:
 *   - Idempotent: repeated calls with the same parameters have no
 *     additional side effects.
 *   - RLS-safe: operates on a single payment row by primary key and
 *     relies on database-enforced visibility rules.
 *   - Transactional: intended to be invoked as part of a larger
 *     domain operation (e.g. session cancellation).
 *
 * Behavior:
 *   - Reads the payment identified by p_payment_id.
 *   - Creates a corresponding credit_ledger entry using the payment's
 *     user, amount, and currency.
 *   - Skips insertion if a credit entry with the same payment_id and
 *     cause already exists.
 *
 * Parameters:
 *   - p_payment_id: Identifier of the payment being credited.
 *   - p_cause: Domain cause for the credit (e.g. 'session_cancelled').
 *
 * Preconditions:
 *   - The payment must exist.
 *   - The caller must be authorized to read the payment under RLS.
 *
 * Postconditions:
 *   - At most one credit_ledger row exists for (payment_id, cause).
 *
 * Notes:
 *   - This function performs no permission checks beyond those enforced
 *     by RLS and table constraints.
 *   - Absence of a visible payment row results in a no-op.
 */
BEGIN
    INSERT INTO app.credit_ledger (
        id,
        user_id,
        amount_cents,
        currency,
        cause,
        payment_id
    )
    SELECT
        gen_random_uuid(),
        p.user_id,
        p.amount_cents,
        p.currency,
        p_cause,
        p.id
    FROM app.payments p
    WHERE p.id = p_payment_id
      AND NOT EXISTS (
          SELECT 1
          FROM app.credit_ledger cl
          WHERE cl.payment_id = p_payment_id
            AND cl.cause = p_cause
      );
END;
$$;

COMMENT ON FUNCTION app_fcn.issue_credit_for_payment(uuid, app.credit_ledger_cause)
IS
'Idempotently issues a credit ledger entry for a specific payment and cause.
Reads payment data by primary key and inserts a corresponding credit entry
only if one does not already exist. Intended for internal domain workflows
such as session cancellation, and safe to call repeatedly.';

