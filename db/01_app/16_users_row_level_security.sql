-- ------------------------------------------------------------------
-- Table: app.users
-- Row Level Security (RLS)
--
-- Purpose:
-- - Restrict access to user records
-- - Enforce self-service rules and admin authority
-- - Prevent privilege escalation
-- ------------------------------------------------------------------

-- Enable RLS on users table
ALTER TABLE app.users ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owner
ALTER TABLE app.users FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: users_select_self_or_admin
--
-- Allows:
-- - Users to read their own user record
-- - Admins to read any user record
-- ------------------------------------------------------------------

CREATE POLICY users_select_self_or_admin
ON app.users
FOR SELECT
USING (
    -- User can read their own record
    id = current_setting('app.current_user_id')::uuid

    -- Admins can read all users
    OR EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY users_select_self_or_admin ON app.users IS
'Allows users to read their own record and admins to read all users.';

-- ------------------------------------------------------------------
-- Policy: users_self_update_profile
--
-- Allows:
-- - Users to update their own profile data
--
-- Restrictions:
-- - Only if the account is not disabled
-- - Does not allow changing disabled state
-- ------------------------------------------------------------------

CREATE POLICY users_self_update_profile
ON app.users
FOR UPDATE
USING (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL
)
WITH CHECK (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL
);

COMMENT ON POLICY users_self_update_profile ON app.users IS
'Allows users to update their own profile while the account is active.';

-- ------------------------------------------------------------------
-- Policy: users_self_delete
--
-- Semantic note:
-- - This is a soft-delete via disabling the account
--
-- Allows:
-- - Users to self-disable their account
--
-- Restrictions:
-- - User must not be an admin
-- - Account must be active before disabling
-- - Disabled reason must be "self"
-- ------------------------------------------------------------------

CREATE POLICY users_self_delete
ON app.users
FOR UPDATE
USING (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL

    -- Admins are not allowed to self-disable via this path
    AND NOT EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
)
WITH CHECK (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NOT NULL
    AND disabled_reason = 'self'
);

COMMENT ON POLICY users_self_delete ON app.users IS
'Allows non-admin users to self-disable their account (soft delete).';

-- ------------------------------------------------------------------
-- Policy: users_admin_update_others
--
-- Allows:
-- - Admins to disable other users
--
-- Restrictions:
-- - Admin cannot modify their own record
-- - Admin actions must explicitly disable the account
-- - disabled_reason must be "admin"
-- ------------------------------------------------------------------

CREATE POLICY users_admin_update_others
ON app.users
FOR UPDATE
USING (
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
    AND id <> current_setting('app.current_user_id')::uuid
)
WITH CHECK (
    disabled_at IS NOT NULL
    AND disabled_reason = 'admin'
);

COMMENT ON POLICY users_admin_update_others ON app.users IS
'Allows admins to disable other users; admin actions must explicitly mark admin responsibility.';

-- ------------------------------------------------------------------
-- Policy: users_select_system
--
-- Purpose:
-- - Allow system-level operations (authentication)
-- - Used during login before user context exists
-- ------------------------------------------------------------------

CREATE POLICY users_select_system
ON app.users
FOR SELECT
TO app_system
USING (true);

COMMENT ON POLICY users_select_system ON app.users IS
'Allows system role to read user records for authentication and system operations.';

-- ------------------------------------------------------------------
-- Policy: users_insert_system
--
-- Purpose:
-- - Allow system-level user creation during registration
-- - Used before a user context exists (no current_user_id)
--
-- Notes:
-- - Restricted to app_system role only
-- - Required for initial account creation
-- ------------------------------------------------------------------

CREATE POLICY users_insert_system
ON app.users
FOR INSERT
TO app_system
WITH CHECK (true);

COMMENT ON POLICY users_insert_system ON app.users IS
'Allows system role to insert new users during registration before a user context exists.';