\c app

-- ------------------------------------------------------------------
-- Indexes: app.credit_ledger
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Fast lookup of a user's ledger entries
--
-- Used by:
-- - User dashboards
-- - RLS filtering
-- ---------------------------------------------------------------
CREATE INDEX idx_credit_ledger_user_id
ON app.credit_ledger (user_id);

COMMENT ON INDEX app.idx_credit_ledger_user_id IS
'Optimizes queries filtering ledger entries by user_id, the most common access pattern.';

-- ---------------------------------------------------------------
-- Efficient chronological scans per user
--
-- Used by:
-- - Computing balances over time
-- - Historical ledger queries
-- ---------------------------------------------------------------
CREATE INDEX idx_credit_ledger_user_created_at
ON app.credit_ledger (user_id, created_at DESC);

COMMENT ON INDEX app.idx_credit_ledger_user_created_at IS
'Speeds up queries scanning a user''s ledger chronologically, e.g., for balance calculations.';

-- ---------------------------------------------------------------
-- Lookup ledger entries by payment intent
--
-- Used by:
-- - Payment reconciliation
-- - Audits
--
-- Partial index to avoid NULLs
-- ---------------------------------------------------------------
CREATE INDEX idx_credit_ledger_payment_intent_id
ON app.credit_ledger (payment_intent_id)
WHERE payment_intent_id IS NOT NULL;

COMMENT ON INDEX app.idx_credit_ledger_payment_intent_id IS
'Optimizes queries finding ledger entries tied to a specific payment intent for reconciliation or auditing.';

-- ---------------------------------------------------------------
-- Fast lookup for credit ledger entries by cause and recency
-- Used by:
-- - Admin dashboards
-- - Auditing and financial timelines
-- ---------------------------------------------------------------
CREATE INDEX idx_credit_ledger_cause_created_at
ON app.credit_ledger (cause, created_at DESC);

COMMENT ON INDEX app.idx_credit_ledger_cause_created_at IS
'Optimizes queries filtering credit ledger entries by cause and ordering by creation time.';
