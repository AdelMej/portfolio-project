\c app

-- ------------------------------------------------------------------
-- Enum: app.credit_ledger_cause
--
-- Defines the business reason for a credit ledger entry.
-- ------------------------------------------------------------------

CREATE TYPE app.credit_ledger_cause AS ENUM (
    'payment',           -- credits added from a successful payment
    'refund',            -- credits returned after a refund
    'session_usage',     -- credits consumed by attending a session
    'admin_adjustment'   -- manual adjustment by an administrator
);

COMMENT ON TYPE app.credit_ledger_cause IS
'Business cause for a credit ledger entry. Determines accounting semantics and validation rules.';

-- ------------------------------------------------------------------
-- Table: app.credit_ledger
--
-- Purpose:
-- - Source of truth for user credit balance
-- - Append-only financial ledger
--
-- Used for:
-- - billing
-- - refunds
-- - session credit usage
-- - audits and compliance
--
-- Design notes:
-- - Rows are immutable after insertion
-- - Balance is materialized for fast reads
-- - All consistency enforced at database level
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.credit_ledger (
    -- Unique ledger entry identifier
    id UUID PRIMARY KEY,

    -- Owner of the credit balance
    user_id UUID NOT NULL,

    -- reference to a payment
    -- Required for payment / refund causes
    payment_id UUID NULL,

    -- Signed credit delta (in cents)
    -- positive = credit added
    -- negative = credit spent
    amount_cents INTEGER NOT NULL,

    -- Resulting balance after applying this entry
    -- Always >= 0
    balance_after_cents INTEGER NOT NULL,

    -- Business cause for this ledger entry
    cause app.credit_ledger_cause NOT NULL,

    -- Ledger entry creation timestamp (UTC)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_credit_ledger_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id),

    CONSTRAINT fk_credit_ledger_payment_id
        FOREIGN KEY (payment_id)
        REFERENCES app.payments(id),

    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Zero-value ledger entries are forbidden
    CONSTRAINT chk_credit_ledger_amount_not_zero
        CHECK (amount_cents <> 0),

    -- Balance may never become negative
    CONSTRAINT chk_credit_ledger_balance_not_negative
        CHECK (balance_after_cents >= 0),
        
    -- Credit balance can never be null
    CONSTRAINT chk_credit_ledger_balance_non_null
		CHECK (balance_after_cents IS NOT NULL)
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.credit_ledger IS
'Append-only financial ledger tracking all credit movements and resulting balances per user.';

COMMENT ON COLUMN app.credit_ledger.id IS
'Primary identifier for the ledger entry.';

COMMENT ON COLUMN app.credit_ledger.user_id IS
'User whose credit balance is affected by this entry.';

COMMENT ON COLUMN app.credit_ledger.payment_id IS
'payment reference. Required for payment and refund causes.';

COMMENT ON COLUMN app.credit_ledger.amount_cents IS
'Signed credit delta in cents. Positive adds credit, negative consumes credit.';

COMMENT ON COLUMN app.credit_ledger.balance_after_cents IS
'User credit balance after applying this ledger entry.';

COMMENT ON COLUMN app.credit_ledger.cause IS
'Business reason for this credit movement.';

COMMENT ON COLUMN app.credit_ledger.created_at IS
'Timestamp when the ledger entry was created (UTC).';

