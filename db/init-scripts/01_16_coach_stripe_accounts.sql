\c app

-- ------------------------------------------------------------------
-- Table: app.coach_stripe_accounts
--
-- Purpose:
-- - Stores Stripe Connect account linkage for coaches
-- - Mirrors Stripe capability state required to receive payments
--
-- Design principles:
-- - One Stripe account per coach (user)
-- - Coach is a derived role, not a first-class entity
-- - Stripe is the source of truth for capability state
-- - No destructive operations (append-only audit elsewhere)
--
-- Notes:
-- - coach_id references app.users(id); coach role enforced via RLS
-- - Capability flags are updated exclusively via Stripe webhooks
-- - This table answers: "Can this coach receive payments?"
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.coach_stripe_accounts (
    -- ------------------------------------------------------------------
    -- Identity
    -- ------------------------------------------------------------------

    coach_id UUID NOT NULL,

    -- ------------------------------------------------------------------
    -- Stripe account linkage
    -- ------------------------------------------------------------------

    stripe_account_id TEXT NOT NULL,

    -- ------------------------------------------------------------------
    -- Stripe capability state (mirrored from webhooks)
    -- ------------------------------------------------------------------

    charges_enabled   BOOLEAN NOT NULL DEFAULT FALSE,
    payouts_enabled   BOOLEAN NOT NULL DEFAULT FALSE,
    details_submitted BOOLEAN NOT NULL DEFAULT FALSE,

    -- ------------------------------------------------------------------
    -- Timestamps
    -- ------------------------------------------------------------------

    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),

    -- ------------------------------------------------------------------
    -- Constraints
    -- ------------------------------------------------------------------

    -- One Stripe account per coach
    CONSTRAINT pk_coach_stripe_accounts
        PRIMARY KEY (coach_id),

    -- Coach must reference a valid user
    CONSTRAINT fk_coach_stripe_accounts_user
        FOREIGN KEY (coach_id)
        REFERENCES app.users(id)
        ON DELETE RESTRICT,

    -- Stripe account IDs must be globally unique
    CONSTRAINT uq_coach_stripe_accounts_stripe_account
        UNIQUE (stripe_account_id),

    -- Stripe account ID must not be empty
    CONSTRAINT chk_coach_stripe_accounts_stripe_account_not_empty
        CHECK (stripe_account_id <> '')
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.coach_stripe_accounts IS
'Stripe Connect account linkage for coaches. Mirrors Stripe capability state required to determine whether a coach can receive payments. One row per coach.';

COMMENT ON COLUMN app.coach_stripe_accounts.coach_id IS
'User ID of the coach. References app.users(id). Coach role is enforced via RLS, not schema.';

COMMENT ON COLUMN app.coach_stripe_accounts.stripe_account_id IS
'Stripe Connect account identifier (e.g., acct_...). Unique across the system.';

COMMENT ON COLUMN app.coach_stripe_accounts.charges_enabled IS
'Whether the Stripe account is allowed to create charges. Mirrored from Stripe webhooks.';

COMMENT ON COLUMN app.coach_stripe_accounts.payouts_enabled IS
'Whether the Stripe account is allowed to receive payouts. Mirrored from Stripe webhooks.';

COMMENT ON COLUMN app.coach_stripe_accounts.details_submitted IS
'Whether all required onboarding details have been submitted to Stripe.';

COMMENT ON COLUMN app.coach_stripe_accounts.created_at IS
'Timestamp when the Stripe account linkage was created.';

COMMENT ON COLUMN app.coach_stripe_accounts.updated_at IS
'Timestamp of last modification. Maintained via trigger.';
