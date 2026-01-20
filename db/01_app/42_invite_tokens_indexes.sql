-- ------------------------------------------------------------------
-- Indexes: app.invite_tokens
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Expired but unused tokens
--
-- Used by:
-- - cleanup routines
-- - audit scripts
--
-- Partial index keeps index size minimal
-- ---------------------------------------------------------------
CREATE INDEX idx_invite_tokens_expired_unused
ON app.invite_tokens (expires_at)
WHERE used_at IS NULL;

COMMENT ON INDEX app.idx_invite_tokens_expired_unused IS
'Optimizes queries to find expired tokens that have not been used yet.';

-- ---------------------------------------------------------------
-- Used tokens
--
-- Used by:
-- - audit scripts
-- - reporting
--
-- Partial index keeps index size minimal
-- ---------------------------------------------------------------
CREATE INDEX idx_invite_tokens_used
ON app.invite_tokens (used_at)
WHERE used_at IS NOT NULL;

COMMENT ON INDEX app.idx_invite_tokens_used IS
'Optimizes queries to find tokens that have already been used.';

-- ---------------------------------------------------------------
-- Fast lookup by token hash
--
-- Used by:
-- - validation during signup
-- - token redemption
-- ---------------------------------------------------------------
CREATE INDEX idx_invite_tokens_token_hash
ON app.invite_tokens (token_hash);

COMMENT ON INDEX app.idx_invite_tokens_token_hash IS
'Supports fast lookup of invite tokens by their hash.';
