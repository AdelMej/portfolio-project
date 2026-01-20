\c app

-- ------------------------------------------------------------------
-- Table: app.invite_tokens
--
-- Purpose:
-- - Stores one-time invitation tokens
-- - Enables controlled user onboarding
-- - Prevents token reuse and expired invites
--
-- Used for:
-- - invite-based registration
-- - admin-issued access
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.invite_tokens (
    -- Unique invite identifier
    id UUID PRIMARY KEY,

    -- Hashed invite token (never store raw token)
    token_hash TEXT NOT NULL,

    -- Expiration timestamp
    expires_at TIMESTAMPTZ NOT NULL,

    -- Timestamp when the invite was consumed
    used_at TIMESTAMPTZ,

    -- Audit fields
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- User who generated the invite (optional)
    created_by UUID,

    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Token hashes must be globally unique
    CONSTRAINT uq_invite_tokens_token_hash
        UNIQUE (token_hash),

    -- Expiration must be after creation
    CONSTRAINT chk_invite_tokens_expires_after_creation
        CHECK (expires_at > created_at),

    -- Invite usage can only occur after creation
    CONSTRAINT chk_invite_tokens_used_after_creation
        CHECK (used_at IS NULL OR used_at >= created_at)
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.invite_tokens IS
'Stores one-time invitation tokens used for controlled user onboarding.';

COMMENT ON COLUMN app.invite_tokens.id IS
'Primary identifier for the invite token.';

COMMENT ON COLUMN app.invite_tokens.token_hash IS
'Hashed value of the invitation token.';

COMMENT ON COLUMN app.invite_tokens.expires_at IS
'Timestamp when the invite token expires and becomes invalid.';

COMMENT ON COLUMN app.invite_tokens.used_at IS
'Timestamp when the invite token was redeemed.';

COMMENT ON COLUMN app.invite_tokens.created_at IS
'Timestamp when the invite token was created.';

COMMENT ON COLUMN app.invite_tokens.created_by IS
'User who generated the invite token, if applicable.';

