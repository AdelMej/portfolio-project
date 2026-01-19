\c app

-- ------------------------------------------------------------------
-- Triggers: app.refresh_tokens
--
-- Purpose:
-- - Enforce immutability of key fields
-- - Prevent un-revoking and post-revocation modifications
--
-- Guarantees:
-- - token_hash and user_id are immutable
-- - revoked tokens cannot be un-revoked
-- - expires_at and replaced_by_token cannot be modified after revocation
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: prevent token_hash modification
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_refresh_tokens_immutable_hash()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.token_hash <> OLD.token_hash THEN
        RAISE EXCEPTION 'refresh_tokens.token_hash is immutable';
    END IF;
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_refresh_tokens_immutable_hash() IS
'Prevents modification of token_hash after creation.';

-- ------------------------------------------------------------------
-- Trigger: enforce immutable token_hash
-- ------------------------------------------------------------------
CREATE TRIGGER trg_refresh_tokens_immutable_hash
BEFORE UPDATE ON app.refresh_tokens
FOR EACH ROW
EXECUTE FUNCTION app.tg_refresh_tokens_immutable_hash();

COMMENT ON TRIGGER trg_refresh_tokens_immutable_hash ON app.refresh_tokens IS
'Blocks any attempt to change token_hash after creation.';

-- ------------------------------------------------------------------
-- Function: prevent user_id modification
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_refresh_tokens_immutable_user()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.user_id <> OLD.user_id THEN
        RAISE EXCEPTION 'refresh_tokens.user_id is immutable';
    END IF;
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_refresh_tokens_immutable_user() IS
'Prevents modification of user_id after creation.';

-- ------------------------------------------------------------------
-- Trigger: enforce immutable user_id
-- ------------------------------------------------------------------
CREATE TRIGGER trg_refresh_tokens_immutable_user
BEFORE UPDATE ON app.refresh_tokens
FOR EACH ROW
EXECUTE FUNCTION app.tg_refresh_tokens_immutable_user();

COMMENT ON TRIGGER trg_refresh_tokens_immutable_user ON app.refresh_tokens IS
'Blocks any attempt to change user_id after creation.';

-- ------------------------------------------------------------------
-- Function: prevent un-revoking and post-revocation changes
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_refresh_tokens_no_unrevoke()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    -- Cannot un-revoke a token
    IF OLD.revoked_at IS NOT NULL AND NEW.revoked_at IS NULL THEN
        RAISE EXCEPTION 'refresh_tokens cannot be un-revoked';
    END IF;

    -- Once revoked, expires_at cannot be modified
    IF OLD.revoked_at IS NOT NULL AND NEW.expires_at <> OLD.expires_at THEN
        RAISE EXCEPTION 'Cannot modify expires_at after token is revoked';
    END IF;

    -- Once revoked, replaced_by_token cannot be modified
    IF OLD.revoked_at IS NOT NULL AND NEW.replaced_by_token <> OLD.replaced_by_token THEN
        RAISE EXCEPTION 'Cannot modify replaced_by_token after token is revoked';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_refresh_tokens_no_unrevoke() IS
'Prevents un-revoking tokens and any modification to expires_at or replaced_by_token after revocation.';

-- ------------------------------------------------------------------
-- Trigger: enforce revoked token immutability
-- ------------------------------------------------------------------
CREATE TRIGGER trg_refresh_tokens_no_unrevoke
BEFORE UPDATE ON app.refresh_tokens
FOR EACH ROW
EXECUTE FUNCTION app.tg_refresh_tokens_no_unrevoke();

COMMENT ON TRIGGER trg_refresh_tokens_no_unrevoke ON app.refresh_tokens IS
'Blocks un-revoking and prevents modifications to key fields after a token is revoked.';
