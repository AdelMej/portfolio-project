\c app

-- ------------------------------------------------------------------
-- Indexes: app.payment_intents
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Fast lookup by user
--
-- Used by:
-- - RLS filters for app_user
-- - User dashboards / payment history
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_user_id
ON app.payment_intents (user_id);

COMMENT ON INDEX app.idx_payment_intents_user_id IS
'Optimizes queries filtering payment intents by user_id (RLS, dashboards).';

-- ---------------------------------------------------------------
-- Fast lookup by session
--
-- Used by:
-- - Joins with sessions
-- - Analytics / refunds
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_session_id
ON app.payment_intents (session_id);

COMMENT ON INDEX app.idx_payment_intents_session_id IS
'Optimizes joins and queries filtering payment intents by session_id.';

-- ---------------------------------------------------------------
-- Admin / ops filtering by status
--
-- Used by:
-- - Admin dashboards
-- - Workflow management
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_status
ON app.payment_intents (status);

COMMENT ON INDEX app.idx_payment_intents_status IS
'Supports filtering payment intents by status (scheduled, completed, etc.).';

-- ---------------------------------------------------------------
-- Time-based queries
--
-- Used by:
-- - Dashboards
-- - Cleanup scripts
-- - Analytics
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_created_at
ON app.payment_intents (created_at);

COMMENT ON INDEX app.idx_payment_intents_created_at IS
'Optimizes queries ordered or filtered by creation time.';

-- ---------------------------------------------------------------
-- Compound: status + created_at
--
-- Used by:
-- - Admin dashboards combining status + recent activity
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_status_created_at
ON app.payment_intents (status, created_at);

COMMENT ON INDEX app.idx_payment_intents_status_created_at IS
'Optimizes combined filtering on status and creation timestamp.';

-- ---------------------------------------------------------------
-- Optional: provider + provider_intent_id
--
-- Supports idempotency and uniqueness enforcement
-- ---------------------------------------------------------------
CREATE INDEX idx_payment_intents_provider_intent
ON app.payment_intents (provider, provider_intent_id);

COMMENT ON INDEX app.idx_payment_intents_provider_intent IS
'Speeds up lookups and enforces idempotency by provider and provider_intent_id.';
