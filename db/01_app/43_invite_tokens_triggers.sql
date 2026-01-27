-- ------------------------------------------------------------------
-- Triggers: app.invite_tokens
--
-- Purpose:
-- - Enforce append-only lifecycle
-- - Guarantee immutability of token fields after creation
--
-- Guarantees:
-- - Only `used_at` may ever be updated
-- - `used_at` cannot be unset once set
-- - All other fields are immutable
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: enforce lifecycle-only updates
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_invite_tokens_update_lifecycle_only()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    --------------------------------------------------------------------------
    -- LIFECYCLE TRANSITION CHECK
    -- Allow update ONLY if the change concerns `used_at`
    --------------------------------------------------------------------------
    IF NEW.used_at IS DISTINCT FROM OLD.used_at THEN
        -- Prevent setting used_at back to NULL
        IF OLD.used_at IS NOT NULL AND NEW.used_at IS NULL THEN
            RAISE EXCEPTION 'Cannot unset used_at once it has been set';
        END IF;

        RETURN NEW;
    END IF;

    --------------------------------------------------------------------------
    -- IMMUTABILITY ENFORCEMENT
    -- Any other modification attempt is forbidden
    --------------------------------------------------------------------------
    RAISE EXCEPTION 'Only used_at may be updated on invite tokens';
END;
$$;

COMMENT ON FUNCTION app.tg_invite_tokens_update_lifecycle_only() IS
'Enforces that invite token rows are append-only; only used_at may be updated and cannot be unset once set.';

-- ------------------------------------------------------------------
-- Trigger: enforce lifecycle-only updates
-- ------------------------------------------------------------------
CREATE TRIGGER trg_invite_tokens_lifecycle_only
BEFORE UPDATE ON app.invite_tokens
FOR EACH ROW
EXECUTE FUNCTION app.tg_invite_tokens_update_lifecycle_only();

COMMENT ON TRIGGER trg_invite_tokens_lifecycle_only ON app.invite_tokens IS
'Prevents modification of any column other than used_at on invite tokens; used_at cannot be reverted to NULL.';
