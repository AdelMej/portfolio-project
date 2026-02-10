\c app

-- ------------------------------------------------------------------
-- Table: app.payment
--
-- Purpose:
-- - Records finalized payments made by users
-- - Represents provider-confirmed monetary transactions
--
-- Used for:
-- - billing records
-- - reconciliation with payment providers
-- - audit and dispute resolution
--
-- Design notes:
-- - One row per successful payment
-- - Idempotency enforced via provider identifiers
-- - Immutable after insertion
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.payments (
    -- Unique internal payment identifier
    id UUID PRIMARY KEY,
    
    -- Session the payment is associated with
    session_id UUID NOT NULL,

    -- User who made the payment
    user_id UUID NOT NULL,
    
    -- Payment provider (e.g. stripe, paypal)
    provider TEXT NOT NULL,

    -- Provider-side payment identifier
    provider_payment_id TEXT NOT NULL,
    
    -- Payment amount in cents
    amount_cents INTEGER NOT NULL,

    -- ISO 4217 currency code (e.g. EUR, USD)
    currency CHAR(3) NOT NULL,
    
    -- Payment creation timestamp (UTC)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- ------------------------------------------------------------------
    -- Uniqueness / idempotency
    -- ------------------------------------------------------------------

    -- Prevent duplicate provider payments
    CONSTRAINT uq_payment_provider_id
        UNIQUE (provider, provider_payment_id),
        
    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_payment_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id),
        
    CONSTRAINT fk_payment_session_id
        FOREIGN KEY (session_id)
        REFERENCES app.sessions(id),
        
    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Payment amount must be strictly positive
    CONSTRAINT chk_payment_amount_positive
        CHECK (amount_cents > 0),
        
    -- Enforce uppercase 3-letter currency code
    CONSTRAINT chk_payment_currency_format
        CHECK (currency ~ '^[A-Z]{3}$')
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.payments IS
'Records finalized, provider-confirmed payments made by users.';

COMMENT ON COLUMN app.payments.id IS
'Primary identifier for the payment record.';

COMMENT ON COLUMN app.payments.session_id IS
'Session for which the payment was made.';

COMMENT ON COLUMN app.payments.user_id IS
'User who initiated and owns the payment.';

COMMENT ON COLUMN app.payments.provider IS
'External payment provider handling the transaction.';

COMMENT ON COLUMN app.payments.provider_payment_id IS
'Unique payment identifier provided by the payment provider.';

COMMENT ON COLUMN app.payments.amount_cents IS
'Payment amount expressed in cents.';

COMMENT ON COLUMN app.payments.currency IS
'ISO 4217 three-letter currency code.';

COMMENT ON COLUMN app.payments.created_at IS
'Timestamp when the payment record was created (UTC).';
