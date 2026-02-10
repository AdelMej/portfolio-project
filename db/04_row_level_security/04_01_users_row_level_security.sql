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
	app_fcn.is_self(id)
    OR app_fcn.is_admin()
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

CREATE POLICY users_self_update
ON app.users
FOR UPDATE
USING (
    app_fcn.is_self(id)
    AND disabled_at IS NULL
)
WITH CHECK (
    app_fcn.is_self(id)
    AND disabled_at IS NULL
);

COMMENT ON POLICY users_self_update ON app.users IS
'Allows users to update their own profile while the account is active.';

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
    app_fcn.is_admin()
    AND NOT app_fcn.is_self(id)
)
WITH CHECK (
    disabled_at IS NOT NULL
    AND disabled_reason = 'admin'
    AND app_fcn.is_admin()
);

COMMENT ON POLICY users_admin_update_others ON app.users IS
'Allows admins to disable other users; admin actions must explicitly mark admin responsibility.';

-- ------------------------------------------------------------------
-- Policy: users_admin_reenable
--
-- Purpose:
-- - Allows admins to re-enable users previously disabled by an admin
-- - Prevents admins from re-enabling themselves
-- - Only applies to users disabled with reason = 'admin'
-- ------------------------------------------------------------------
CREATE POLICY users_admin_reenable
ON app.users
FOR UPDATE
USING (
	app_fcn.is_admin()
    AND NOT app_fcn.is_self(id)
    AND disabled_reason = 'admin'
)
WITH CHECK (
    disabled_at IS NULL
    AND disabled_reason IS NULL
);

COMMENT ON POLICY users_admin_reenable ON app.users IS
'Allows admins to re-enable users disabled by an admin; self re-enable is forbidden and state must be fully cleared.';
