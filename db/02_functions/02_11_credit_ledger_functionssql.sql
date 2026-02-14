CREATE OR REPLACE FUNCTION app_fcn.fetch_credit_fcn(
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

COMMENT ON FUNCTION app_fcn.fetch_credit_fcn(uuid, text) IS
'Returns the current credit balance (in cents) for a user and currency
by summing all entries in the credit ledger.

The balance is derived, authoritative, and based on an append-only
ledger model.

Authorization:
- Users may fetch their own credit balance
- Admins may fetch any user credit balance.';

