create or replace function app_fcn.intent_exists(
	p_provider_payment_id text
)
returns boolean
language sql
security definer
stable
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * intent_exists
	 * -------------
	 * Checks whether a payment intent exists for the given provider intent ID.
	 *
	 * This function performs a simple existence check against the
	 * `app.payment_intents` table using the provider-side identifier.
	 *
	 * Parameters:
	 *   p_provider_payment_id (text)
	 *     The payment intent identifier as provided by the payment provider
	 *     (e.g. Stripe payment_intent.id).
	 *
	 * Returns:
	 *   boolean
	 *     TRUE  if a matching payment intent exists
	 *     FALSE otherwise
	 *
	 * Notes:
	 * - This function does not perform any permission checks
	 * - Does not raise if the intent does not exist
	 * - Intended for idempotency guards and webhook filtering
	 * - Marked STABLE as it performs a read-only lookup
	 */
	SELECT EXISTS(
		SELECT 1
		FROM app.payment_intents
		WHERE provider_intent_id = p_provider_payment_id
	)
$$;

COMMENT ON FUNCTION app_fcn.intent_exists(text)
IS 'Returns true if a payment intent exists for the given provider intent ID.';

