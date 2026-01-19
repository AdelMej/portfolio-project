-- ------------------------------------------------------------------
-- Table: app.refresh_tokens
--
-- Purpose:
-- - Stores long-lived authentication refresh tokens
-- - Enables secure session renewal
-- - Supports token rotation and revocation
--
-- Used for:
-- - maintaining user login sessions
-- - detecting token reuse
-- - enforcing logout across devices
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.refresh_tokens (
    -- Surrogate identifier (monotonic, ordered)
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Owner of the refresh token
    user_id UUID NOT NULL,

    -- Hashed refresh token value
    token_hash TEXT NOT NULL,
    
    -- Token creation timestamp
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Token expiration timestamp
    expires_at TIMESTAMPTZ NOT NULL,

    -- Timestamp when token was explicitly revoked
    revoked_at TIMESTAMPTZ,

    -- Token rotation pointer (next token in chain)
    replaced_by_token BIGINT,
    
    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_refresh_tokens_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_refresh_tokens_replaced_by
        FOREIGN KEY (replaced_by_token)
        REFERENCES app.refresh_tokens(id),

    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Token hashes must be globally unique
    CONSTRAINT uq_refresh_tokens_token_hash
        UNIQUE (token_hash),

    -- Expiration must be after creation
    CONSTRAINT chk_refresh_tokens_expiry
        CHECK (expires_at > created_at),

    -- Revocation can only happen after creation
    CONSTRAINT chk_revoked_after_creation
        CHECK (revoked_at IS NULL OR revoked_at >= created_at)
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.refresh_tokens IS
'Stores refresh tokens for authentication, supporting rotation, revocation, and session invalidation.';

COMMENT ON COLUMN app.refresh_tokens.id IS
'Surrogate primary key for refresh tokens, used for ordering and rotation chains.';

COMMENT ON COLUMN app.refresh_tokens.user_id IS
'User who owns this refresh token.';

COMMENT ON COLUMN app.refresh_tokens.token_hash IS
'Hashed value of the refresh token (never store raw tokens).';

COMMENT ON COLUMN app.refresh_tokens.created_at IS
'Timestamp when the refresh token was created.';

COMMENT ON COLUMN app.refresh_tokens.expires_at IS
'Timestamp when the refresh token expires and becomes invalid.';

COMMENT ON COLUMN app.refresh_tokens.revoked_at IS
'Timestamp when the refresh token was explicitly revoked.';

COMMENT ON COLUMN app.refresh_tokens.replaced_by_token IS
'Reference to the next refresh token generated during token rotation.';
