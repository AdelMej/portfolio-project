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
