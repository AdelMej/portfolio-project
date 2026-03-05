\c app

-- ------------------------------------------------------------------
-- Indexes: app.users
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Admin listings / audits
--
-- Used by:
-- - admin dashboards
-- - chronological user listings
-- ---------------------------------------------------------------

CREATE INDEX idx_users_created_at
ON app.users (created_at DESC);

COMMENT ON INDEX app.idx_users_created_at IS
'Supports admin listing and auditing of users by creation time.';

-- ---------------------------------------------------------------
-- Disabled users lookup
--
-- Used by:
-- - admin tooling
-- - compliance / cleanup workflows
--
-- Partial index keeps size minimal
-- ---------------------------------------------------------------

CREATE INDEX idx_users_disabled_at
ON app.users (disabled_at)
WHERE disabled_at IS NOT NULL;

COMMENT ON INDEX app.idx_users_disabled_at IS
'Optimizes queries targeting disabled users only.';
