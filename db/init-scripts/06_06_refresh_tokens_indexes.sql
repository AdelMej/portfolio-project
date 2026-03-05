\c app

-- ------------------------------------------------------------------
-- Indexes: app.refresh_tokens
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- User token lookup
--
-- Used by:
-- - Listing tokens for a specific user
-- - RLS enforcement on queries
-- ---------------------------------------------------------------
CREATE INDEX idx_refresh_tokens_user_id
ON app.refresh_tokens (user_id);

COMMENT ON INDEX app.idx_refresh_tokens_user_id IS
'Supports fast lookups of refresh tokens by user_id for queries and RLS enforcement.';

-- ---------------------------------------------------------------
-- Active tokens lookup
--
-- Used by:
-- - Cleanup of expired/revoked tokens
-- - Session management
--
-- Partial index for performance (only active tokens)
-- ---------------------------------------------------------------
CREATE INDEX idx_refresh_tokens_active
ON app.refresh_tokens (expires_at)
WHERE revoked_at IS NULL;

COMMENT ON INDEX app.idx_refresh_tokens_active IS
'Optimizes queries filtering only active (non-revoked) refresh tokens.';

-- ---------------------------------------------------------------
-- Token replacement chain inspection
--
-- Used by:
-- - Detecting token rotations
-- - Security audits
-- ---------------------------------------------------------------
CREATE INDEX idx_refresh_tokens_replaced_by
ON app.refresh_tokens (replaced_by_token_id);

COMMENT ON INDEX app.idx_refresh_tokens_replaced_by IS
'Supports fast lookups of tokens replaced by other tokens (rotation chain).';

-- ------------------------------------------------------------------
-- Indexes: app.invite_tokens
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Expiration-based cleanup
--
-- Used by:
-- - Deleting expired invite tokens
-- - Scheduling reminders / cleanups
-- ---------------------------------------------------------------
CREATE INDEX idx_invite_tokens_expires_at
ON app.invite_tokens (expires_at);

COMMENT ON INDEX app.idx_invite_tokens_expires_at IS
'Supports fast queries on invite tokens by expiration date.';

-- ---------------------------------------------------------------
-- Used tokens lookup
--
-- Used by:
-- - Preventing reuse of already used invite tokens
-- ---------------------------------------------------------------
CREATE INDEX idx_invite_tokens_used_at
ON app.invite_tokens (used_at)
WHERE used_at IS NOT NULL;

COMMENT ON INDEX app.idx_invite_tokens_used_at IS
'Optimizes queries targeting invite tokens that have been used.';