-- ------------------------------------------------------------------
-- Extension: citext
--
-- Purpose:
-- - Provides case-insensitive text type (CITEXT)
-- - Enables semantic equality for user-facing identifiers
--
-- Typical use cases:
-- - Email addresses
-- - Usernames
-- - Invite codes
-- - Any value where case should not affect uniqueness or comparison
--
-- Rationale:
-- - Avoids LOWER() hacks and functional indexes
-- - Enforces correctness at the type level
-- - Plays nicely with UNIQUE constraints
-- ------------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS citext;

COMMENT ON EXTENSION citext IS
'Case-insensitive text type. Used for user-facing identifiers such as emails and usernames where case must not affect equality or uniqueness.';