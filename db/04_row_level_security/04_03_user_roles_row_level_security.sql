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

CREATE POLICY user_roles_visible
ON app.user_roles
FOR SELECT
USING (
    -- Self
    app_fcn.is_self(user_id)

    OR

    -- App-level admin
    app_fcn.is_admin()
);
