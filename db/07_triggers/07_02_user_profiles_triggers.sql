-- ------------------------------------------------------------------
-- Triggers: app.user_profiles
--
-- Purpose:
-- - Enforce profile immutability rules
-- - Maintain audit consistency
--
-- Guarantees:
-- - user_id can never be changed after creation
-- - updated_at is always refreshed on UPDATE
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: auto-update updated_at
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_user_profiles_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_user_profiles_set_updated_at() IS
'Automatically updates updated_at timestamp on every profile update.';

-- ------------------------------------------------------------------
-- Trigger: set updated_at on update
-- ------------------------------------------------------------------

CREATE TRIGGER trg_10_user_profiles_set_updated_at
BEFORE UPDATE ON app.user_profiles
FOR EACH ROW
EXECUTE FUNCTION app.tg_user_profiles_set_updated_at();

COMMENT ON TRIGGER trg_10_user_profiles_set_updated_at ON app.user_profiles IS
'Ensures updated_at reflects the last modification time.';

-- ------------------------------------------------------------------
-- Function: prevent user_id mutation
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_user_profiles_immutable_user_id()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.user_id <> OLD.user_id THEN
        RAISE EXCEPTION
            'user_profiles.user_id is immutable (old=%, new=%)',
            OLD.user_id, NEW.user_id;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_user_profiles_immutable_user_id() IS
'Prevents reassignment of a profile to another user. user_id is immutable.';

-- ------------------------------------------------------------------
-- Trigger: enforce immutable user_id
-- ------------------------------------------------------------------

CREATE TRIGGER trg_20_user_profiles_immutable_user_id
BEFORE UPDATE ON app.user_profiles
FOR EACH ROW
EXECUTE FUNCTION app.tg_user_profiles_immutable_user_id();

COMMENT ON TRIGGER trg_20_user_profiles_immutable_user_id ON app.user_profiles IS
'Blocks any attempt to change user_profiles.user_id after creation.';
