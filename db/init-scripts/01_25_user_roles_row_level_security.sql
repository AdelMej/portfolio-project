\c app

-- ------------------------------------------------------------------
-- Row Level Security: app.user_roles
--
-- Controls visibility and lifecycle of user ↔ role assignments.
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.user_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.user_roles FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- SELECT
--
-- - Users can see their own roles
-- - App-level admins can see all role assignments
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.is_admin(_user_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = app
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = _user_id
          AND r.role_name = 'admin'
    );
$$;

CREATE POLICY user_roles_visible
ON app.user_roles
FOR SELECT
USING (
    -- Self
    user_id = current_setting('app.current_user_id')::uuid

    OR

    -- App-level admin
    app.is_admin(current_setting('app.current_user_id')::uuid)
);

-- ------------------------------------------------------------------
-- INSERT
--
-- - app_system may assign roles freely
-- - app-level admins may assign roles
-- ------------------------------------------------------------------

CREATE POLICY user_roles_system_insert
ON app.user_roles
FOR INSERT
TO app_system
WITH CHECK (TRUE);

CREATE POLICY user_roles_admin_insert
ON app.user_roles
FOR INSERT
TO app_user
WITH CHECK (
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

-- ------------------------------------------------------------------
-- DELETE
--
-- - app_system may revoke roles freely
-- - app-level admins may revoke roles
-- - admins may NOT remove their own admin role
-- ------------------------------------------------------------------

CREATE POLICY user_roles_admin_or_system_delete
ON app.user_roles
FOR DELETE
USING (
    (
        -- app_system
        pg_has_role(current_user, 'app_system', 'member')

        OR

        -- app-level admin
        EXISTS (
            SELECT 1
            FROM app.user_roles ur
            JOIN app.roles r ON r.id = ur.role_id
            WHERE ur.user_id = current_setting('app.current_user_id')::uuid
              AND r.role_name = 'admin'
        )
    )
    AND NOT (
        -- prevent self-removal of admin role
        user_id = current_setting('app.current_user_id')::uuid
        AND EXISTS (
            SELECT 1
            FROM app.roles r
            WHERE r.id = role_id
              AND r.role_name = 'admin'
        )
    )
);

