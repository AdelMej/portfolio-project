-- ------------------------------------------------------------------
-- Indexes: app.payment
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Fast lookup by user
--
-- Used by:
-- - RLS filtering
-- - User-centric queries (payment history, dashboards)
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_user_id
ON app.payments (user_id);

COMMENT ON INDEX app.idx_payment_user_id IS
'Optimizes queries filtering or joining payments by user_id.';

-- ---------------------------------------------------------------
-- Fast lookup by session
--
-- Used by:
-- - Session reconciliation
-- - Dashboard reporting
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_session_id
ON app.payments (session_id);

COMMENT ON INDEX app.idx_payment_session_id IS
'Optimizes queries filtering or joining payments by session_id.';

-- ---------------------------------------------------------------
-- Provider + provider_payment_id uniqueness lookup
--
-- Used by:
-- - Idempotency enforcement
-- - Duplicate detection
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_provider_payment_id
ON app.payments (provider, provider_payment_id);

COMMENT ON INDEX app.idx_payment_provider_payment_id IS
'Speeds up lookup of payments by provider and provider_payment_id for idempotency checks.';

-- ---------------------------------------------------------------
-- Time-based queries
--
-- Used by:
-- - Analytics
-- - Reporting
-- - Cleanup or archiving
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_created_at
ON app.payments (created_at);

COMMENT ON INDEX app.idx_payment_created_at IS
'Optimizes queries filtering payments by creation timestamp.';

-- ---------------------------------------------------------------
-- Optional: gross_amount + currency (aggregations, dashboards)
--
-- Used by:
-- - Reporting
-- - Revenue analytics
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_gross_amount_currency
ON app.payments (gross_amount_cents, currency);

COMMENT ON INDEX app.idx_payment_gross_amount_currency IS
'Speeds up queries aggregating payments by gross amount and currency.';

-- ---------------------------------------------------------------
-- Optional: net_amount + currency (aggregations, dashboards)
--
-- Used by:
-- - Reporting
-- - Revenue analytics
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_net_amount_currency
ON app.payments (net_amount_cents, currency);

COMMENT ON INDEX app.idx_payment_net_amount_currency IS
'Speeds up queries aggregating payments by net amount and currency.';

-- ---------------------------------------------------------------
-- Optional: provider fee + currency (aggregations, dashboards)
--
-- Used by:
-- - Reporting
-- - Revenue analytics
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_provider_fee_currency
ON app.payments (provider_fee_cents, currency);

COMMENT ON INDEX app.idx_payment_provider_fee_currency IS
'Speeds up queries aggregating payments by provider fee and currency.'

