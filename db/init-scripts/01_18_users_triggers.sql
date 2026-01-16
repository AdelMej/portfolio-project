\c app

-- function to auto set updated_at
CREATE OR REPLACE FUNCTION app.tg_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- function to prevent double disabling
CREATE OR REPLACE FUNCTION app.tg_prevent_double_disable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.disabled_at IS NOT NULL AND NEW.disabled_at IS NOT NULL THEN
        RAISE EXCEPTION 'User is already disabled';
    END IF;

    RETURN NEW;
END;
$$;

-- trigger to auto update updated_at
CREATE TRIGGER trg_users_set_updated_at
BEFORE UPDATE ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_set_updated_at();

-- trigger to prevent double disabling
CREATE TRIGGER trg_users_prevent_double_disable
BEFORE UPDATE OF disabled_at ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_prevent_double_disable();