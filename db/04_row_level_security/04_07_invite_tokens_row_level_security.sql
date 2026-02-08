-- ------------------------------------------------------------------
-- Row Level Security: app.invite_tokens
--
-- Purpose:
-- - Restrict access to invitation tokens based on role
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.invite_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.invite_tokens FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: app_system full access
--
-- Allows system automation to perform all operations
-- ------------------------------------------------------------------
CREATE POLICY invite_tokens_system_all
ON app.invite_tokens
FOR ALL
TO app_system
USING (true)
WITH CHECK (true);

COMMENT ON POLICY invite_tokens_system_all ON app.invite_tokens IS
'Allows app_system role to insert, update, delete, and select invite tokens.';

-- ------------------------------------------------------------------
-- Policy: admin read
--
-- Admins can read all tokens
-- ------------------------------------------------------------------
CREATE POLICY invite_tokens_admin_read
ON app.invite_tokens
FOR SELECT
TO app_admin
USING (true);

COMMENT ON POLICY invite_tokens_admin_read ON app.invite_tokens IS
'Allows app_admin role to read all invite tokens.';

-- ------------------------------------------------------------------
-- Policy: admin delete
--
-- Admins can delete tokens
-- ------------------------------------------------------------------
CREATE POLICY invite_tokens_admin_delete
ON app.invite_tokens
FOR DELETE
TO app_admin
USING (true);

COMMENT ON POLICY invite_tokens_admin_delete ON app.invite_tokens IS
'Allows app_admin role to delete invite tokens.';

-- ------------------------------------------------------------------
-- Policy: deny access for regular users
--
-- app_user cannot see, modify, or delete any tokens
-- ------------------------------------------------------------------
CREATE POLICY invite_tokens_no_user_access
ON app.invite_tokens
FOR ALL
TO app_user
USING (false);

COMMENT ON POLICY invite_tokens_no_user_access ON app.invite_tokens IS
'Prevents app_user role from accessing invite tokens in any way.';
