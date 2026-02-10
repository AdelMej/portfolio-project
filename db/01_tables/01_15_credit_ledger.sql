-- ------------------------------------------------------------------
-- Enum: app.credit_ledger_cause
--
-- Defines the business reason for a credit ledger entry.
-- ------------------------------------------------------------------

CREATE TYPE app.credit_ledger_cause AS ENUM (
    'session_usage',       -- credits consumed by attending a session
    'session_cancelled',   -- credits restored after a session cancellation
    'admin_adjustment'     -- manual adjustment by an administrator
);

COMMENT ON TYPE app.credit_ledger_cause IS
'Business cause for a credit ledger entry. Represents entitlement changes only; independent of payment or billing systems.';

-- ------------------------------------------------------------------
-- Table: app.credit_ledger
--
-- Purpose:
-- - Source of truth for user credit balances
-- - Append-only entitlement ledger
--
-- Used for:
-- - session credit consumption
-- - credit restoration on session cancellation
-- - administrative credit adjustments
-- - audits and compliance
--
-- Design notes:
-- - Rows are immutable after insertion
-- - Ledger is append-only
-- - Balance is materialized for fast reads
-- - All consistency enforced at database level
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.credit_ledger (
    -- Unique ledger entry identifier
    id UUID PRIMARY KEY,

    -- Owner of the credit balance
    user_id UUID NOT NULL,

    -- Optional reference to a payment (informational only)
    -- Not required for entitlement accounting
    payment_id UUID NULL,

    -- Signed credit delta (in cents)
    -- Positive = credit added
    -- Negative = credit consumed
    amount_cents INTEGER NOT NULL,

    -- Resulting balance after applying this entry
    -- Always >= 0
    balance_after_cents INTEGER NOT NULL,

    -- Business cause for this credit movement
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

    -- Credit balance may never become negative
    CONSTRAINT chk_credit_ledger_balance_not_negative
        CHECK (balance_after_cents >= 0)
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.credit_ledger IS
'Append-only entitlement ledger tracking all credit balance changes per user.';

COMMENT ON COLUMN app.credit_ledger.id IS
'Primary identifier for the credit ledger entry.';

COMMENT ON COLUMN app.credit_ledger.user_id IS
'User whose credit balance is affected by this ledger entry.';

COMMENT ON COLUMN app.credit_ledger.payment_id IS
'Optional reference to an external payment. Not required for entitlement accounting.';

COMMENT ON COLUMN app.credit_ledger.amount_cents IS
'Signed credit delta in cents. Positive adds credit, negative consumes credit.';

COMMENT ON COLUMN app.credit_ledger.balance_after_cents IS
'User credit balance after applying this ledger entry.';

COMMENT ON COLUMN app.credit_ledger.cause IS
'Business reason for this credit balance change.';

COMMENT ON COLUMN app.credit_ledger.created_at IS
'Timestamp when the ledger entry was created (UTC).';
