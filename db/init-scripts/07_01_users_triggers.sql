\c app

-- ------------------------------------------------------------------
-- Function: app.tg_prevent_double_disable
--
-- Purpose:
-- - Prevents disabling a user more than once
-- - Enforces lifecycle immutability once disabled
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_prevent_double_disable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    -- If user is already disabled, block further disable attempts
    IF OLD.disabled_at IS NOT NULL
       AND NEW.disabled_at IS NOT NULL THEN
        RAISE EXCEPTION 'User is already disabled';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_prevent_double_disable IS
'Prevents disabling a user account more than once.';

-- ------------------------------------------------------------------
-- Trigger: trg_10_users_prevent_double_disable
--
-- First line of defense:
-- - Blocks repeated disable attempts early
-- ------------------------------------------------------------------
CREATE TRIGGER trg_10_users_prevent_double_disable
BEFORE UPDATE OF disabled_at ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_prevent_double_disable();

COMMENT ON TRIGGER trg_10_users_prevent_double_disable ON app.users IS
'Prevents disabling a user account more than once.';

-- ------------------------------------------------------------------
-- Function: app.tg_prevent_admin_self_disable
--
-- Purpose:
-- - Prevents admin users from disabling their own account
-- - Avoids accidental system lockout
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_prevent_admin_self_disable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF
        NEW.disabled_at IS NOT NULL
        AND OLD.disabled_at IS NULL
        AND EXISTS (
            SELECT 1
            FROM app.user_roles ur
            JOIN app.roles r ON r.id = ur.role_id
            WHERE ur.user_id = OLD.id
              AND r.role_name = 'admin'
        )
    THEN
        RAISE EXCEPTION 'Admins cannot disable themselves';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_prevent_admin_self_disable IS
'Prevents administrators from disabling their own account.';

-- ------------------------------------------------------------------
-- Trigger: trg_20_users_prevent_admin_self_disable
--
-- Second guard:
-- - Ensures admins cannot self-disable
-- ------------------------------------------------------------------
CREATE TRIGGER trg_20_users_prevent_admin_self_disable
BEFORE UPDATE OF disabled_at ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_prevent_admin_self_disable();

COMMENT ON TRIGGER trg_20_users_prevent_admin_self_disable ON app.users IS
'Blocks administrators from disabling their own account.';

-- ------------------------------------------------------------------
-- Function: app.tg_admin_update_others_lifecycle_only
--
-- Purpose:
-- - Restricts admins to lifecycle-only updates on other users
-- - Admins may ONLY modify disabled_at
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_admin_update_others_lifecycle_only()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id uuid := current_setting('app.current_user_id', true)::uuid;
BEGIN
    -- Only care about UPDATE
    IF TG_OP <> 'UPDATE' THEN
        RETURN NEW;
    END IF;

    -- No user context → system operation → allow
    IF v_user_id IS NULL THEN
        RETURN NEW;
    END IF;

    -- Only apply when current user is an app-level admin
    IF EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = v_user_id
          AND r.role_name = 'admin'
    ) THEN
        -- Only restrict when admin is updating someone else
        IF OLD.id <> v_user_id THEN
            -- Allow ONLY disabled_at to change
            IF NEW.disabled_at IS DISTINCT FROM OLD.disabled_at THEN
                RETURN NEW;
            END IF;

            RAISE EXCEPTION
                'Admins may only modify disabled_at on other users';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_admin_update_others_lifecycle_only IS
'Restricts admin updates on other users to disabled_at only.';

-- ------------------------------------------------------------------
-- Trigger: trg_30_users_admin_update_others_lifecycle_only
--
-- Enforces lifecycle-only admin mutations
-- Logic lives inside the trigger function
-- ------------------------------------------------------------------
CREATE TRIGGER trg_30_users_admin_update_others_lifecycle_only
BEFORE UPDATE ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_admin_update_others_lifecycle_only();

COMMENT ON TRIGGER trg_30_users_admin_update_others_lifecycle_only ON app.users IS
'Restricts admin updates on other users to lifecycle-only changes.';

-- ------------------------------------------------------------------
-- Function: app.tg_set_updated_at
--
-- Purpose:
-- - Automatically refreshes updated_at on any UPDATE
-- - Runs last to reflect final row state
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_users_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    -- Always bump updated_at on row modification
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_users_set_updated_at IS
'Automatically updates updated_at timestamp on row modification.';

-- ------------------------------------------------------------------
-- Trigger: trg_90_users_set_updated_at
--
-- Final step:
-- - Ensures updated_at reflects the final validated state
-- ------------------------------------------------------------------
CREATE TRIGGER trg_90_users_set_updated_at
BEFORE UPDATE ON app.users
FOR EACH ROW
EXECUTE FUNCTION app.tg_users_set_updated_at();

COMMENT ON TRIGGER trg_90_users_set_updated_at ON app.users IS
'Automatically maintains updated_at timestamp on UPDATE.';
