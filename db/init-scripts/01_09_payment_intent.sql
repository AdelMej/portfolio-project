\c app

-- ------------------------------------------------------------------
-- Table: app.payment_intents
--
-- Purpose:
-- - Represents in-progress or pending payment attempts
-- - Tracks interaction with external payment providers
-- - Acts as the bridge between:
--   - external payment lifecycle
--   - internal credit application
--
-- Used for:
-- - payment initiation
-- - webhook reconciliation
-- - retry / idempotency handling
-- - linking finalized payments to credit ledger entries
--
-- Design notes:
-- - One row per provider-side payment intent
-- - Idempotency enforced via provider identifiers
-- - May be updated while pending
-- - Finalized money is recorded separately in app.payment
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.payment_intents (
    -- Unique internal payment intent identifier
    id UUID PRIMARY KEY,
    
    -- User initiating the payment
    user_id UUID NOT NULL,

    -- Session the payment intent is associated with
    session_id UUID NOT NULL,
    
    -- Payment provider (e.g. stripe, paypal)
    provider TEXT NOT NULL,

    -- Provider-side payment intent identifier
    provider_intent_id TEXT NOT NULL,

    -- Current lifecycle status of the intent
    -- (e.g. created, requires_action, succeeded, cancelled, failed)
    status TEXT NOT NULL,

    -- Amount of credits already applied from this intent
    credit_applied_cents INTEGER NOT NULL DEFAULT 0,

    -- Intended payment amount in cents
    amount_cents INTEGER NOT NULL,

    -- ISO 4217 currency code (e.g. EUR, USD)
    currency CHAR(3) NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_payment_intents_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id),
        
    CONSTRAINT fk_payment_intents_session_id
        FOREIGN KEY (session_id)
        REFERENCES app.sessions(id),
        
    -- ------------------------------------------------------------------
    -- Uniqueness / idempotency
    -- ------------------------------------------------------------------

    -- Prevent duplicate intents from the same provider
    CONSTRAINT uq_payment_intents_provider_intent
        UNIQUE (provider, provider_intent_id),
        
    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Provider must not be empty
    CONSTRAINT chk_payment_intents_provider_not_empty
        CHECK (provider <> ''),
        
    -- Provider intent id must not be empty
    CONSTRAINT chk_payment_intents_provider_intent_id_not_empty
        CHECK (provider_intent_id <> ''),
        
    -- Status must not be empty
    CONSTRAINT chk_payment_intents_status_not_empty
        CHECK (status <> ''),
        
    -- At least one of amount or credit application must be positive
    CONSTRAINT chk_payment_intents_amount_positive
        CHECK (amount_cents > 0 OR credit_applied_cents > 0),
        
    -- Enforce uppercase 3-letter currency code
    CONSTRAINT chk_payment_intents_currency_format
        CHECK (currency ~ '^[A-Z]{3}$'),
        
    -- Applied credit must never be negative
    CONSTRAINT chk_payment_intents_credit_non_negative
        CHECK (credit_applied_cents >= 0)
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.payment_intents IS
'Tracks in-progress payment attempts and provider-side payment intent state.';

COMMENT ON COLUMN app.payment_intents.id IS
'Primary identifier for the payment intent.';

COMMENT ON COLUMN app.payment_intents.user_id IS
'User who initiated the payment intent.';

COMMENT ON COLUMN app.payment_intents.session_id IS
'Session associated with this payment intent.';

COMMENT ON COLUMN app.payment_intents.provider IS
'External payment provider handling the transaction.';

COMMENT ON COLUMN app.payment_intents.provider_intent_id IS
'Unique identifier of the payment intent on the provider side.';

COMMENT ON COLUMN app.payment_intents.status IS
'Current lifecycle status of the payment intent.';

COMMENT ON COLUMN app.payment_intents.credit_applied_cents IS
'Amount of credits already applied as part of this intent.';

COMMENT ON COLUMN app.payment_intents.amount_cents IS
'Total intended payment amount expressed in cents.';

COMMENT ON COLUMN app.payment_intents.currency IS
'ISO 4217 three-letter currency code.';

COMMENT ON COLUMN app.payment_intents.created_at IS
'Timestamp when the payment intent was created (UTC).';

COMMENT ON COLUMN app.payment_intents.updated_at IS
'Timestamp when the payment intent was last updated (UTC).';
