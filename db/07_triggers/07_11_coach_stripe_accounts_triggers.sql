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

-- ------------------------------------------------------------------
-- Trigger: prevent stripe_account_id mutation
--
-- Rationale:
-- - stripe_account_id represents a stable external identifier
-- - Changing it would break the association with Stripe
-- - Prevents accidental reassignment due to bugs or bad updates
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.trg_prevent_stripe_account_id_update()
RETURNS trigger AS $$
BEGIN
    IF OLD.stripe_account_id IS NOT NULL
       AND NEW.stripe_account_id <> OLD.stripe_account_id THEN
        RAISE EXCEPTION 'stripe_account_id is immutable';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_prevent_stripe_account_id_update
BEFORE UPDATE ON app.coach_stripe_accounts
FOR EACH ROW
EXECUTE FUNCTION app.trg_prevent_stripe_account_id_update();

COMMENT ON FUNCTION app.trg_prevent_stripe_account_id_update() IS
'Prevents mutation of stripe_account_id after initial assignment.

Enforces immutability of the Stripe external account identifier to
maintain consistency with Stripe state and avoid accidental reassociation.';
