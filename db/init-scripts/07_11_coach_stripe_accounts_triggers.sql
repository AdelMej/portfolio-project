\c app

-- ------------------------------------------------------------------
-- Triggers: app.coach_stripe_accounts
--
-- Purpose:
-- - Maintain authoritative timestamps
-- - Avoid no-op updates from repeated Stripe webhooks
--
-- Design principles:
-- - Stripe is the sole source of truth
-- - Only meaningful state changes should mutate rows
-- - Timestamps are database-controlled
-- ------------------------------------------------------------------


-- ------------------------------------------------------------------
-- Trigger function: touch updated_at on meaningful UPDATE
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_touch_coach_stripe_accounts_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

-- ------------------------------------------------------------------
-- Trigger: update updated_at only when Stripe state changes
--
-- Rationale:
-- - Stripe webhooks may be retried
-- - Prevents no-op updates and timestamp churn
-- ------------------------------------------------------------------
CREATE TRIGGER trg_touch_coach_stripe_accounts_updated_at
BEFORE UPDATE
ON app.coach_stripe_accounts
FOR EACH ROW
WHEN (
    OLD.charges_enabled   IS DISTINCT FROM NEW.charges_enabled OR
    OLD.payouts_enabled   IS DISTINCT FROM NEW.payouts_enabled OR
    OLD.details_submitted IS DISTINCT FROM NEW.details_submitted
)
EXECUTE FUNCTION app.tg_touch_coach_stripe_accounts_updated_at();

COMMENT ON FUNCTION app.tg_touch_coach_stripe_accounts_updated_at() IS
'Trigger function that updates updated_at only when Stripe capability state changes.
Prevents no-op updates and timestamp churn caused by repeated or idempotent Stripe webhooks.';