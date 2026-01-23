-- ------------------------------------------------------------------
-- Row Level Security: app.refresh_tokens
--
-- Purpose:
-- - Protect refresh tokens from unauthorized access
-- - Enforce strict separation between system-level auth flows
--   and user-level visibility
--
-- Visibility model:
-- - Users may view only their own refresh tokens
-- - App-level admins may view all refresh tokens
-- - app_system may view all refresh tokens (pre-auth, refresh, jobs)
--
-- Write model:
-- - Only app_system may create, rotate, or revoke refresh tokens
--
-- Security notes:
-- - User context relies on app.current_user_id
-- - System context must not depend on user session state
-- - Trust boundaries are enforced via separate RLS policies
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.refresh_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.refresh_tokens FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_select_user_admin
--
-- Allows:
-- - Users to read their own refresh tokens
-- - Admins to read all refresh tokens
--
-- Requires:
-- - app.current_user_id to be set (post-auth context)
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_select_user_admin
ON app.refresh_tokens
FOR SELECT
USING (
    user_id = current_setting('app.current_user_id', true)::uuid

    OR

    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id', true)::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY refresh_tokens_select_user_admin ON app.refresh_tokens IS
'Allows users to read their own refresh tokens and admins to read all tokens.';

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_select_system
--
-- Allows:
-- - app_system to read all refresh tokens
--
-- Used for:
-- - login
-- - token refresh
-- - background revocation / cleanup
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_select_system
ON app.refresh_tokens
FOR SELECT
TO app_system
USING (true);

COMMENT ON POLICY refresh_tokens_select_system ON app.refresh_tokens IS
'Allows system role to read all refresh tokens for authentication and maintenance.';

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_system_insert
--
-- Allows:
-- - app_system to create refresh tokens
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_system_insert
ON app.refresh_tokens
FOR INSERT
TO app_system
WITH CHECK (true);

COMMENT ON POLICY refresh_tokens_system_insert ON app.refresh_tokens IS
'Restricts refresh token creation to the system role.';

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_system_update
--
-- Allows:
-- - app_system to rotate or revoke refresh tokens
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_system_update
ON app.refresh_tokens
FOR UPDATE
TO app_system
USING (true)
WITH CHECK (true);

COMMENT ON POLICY refresh_tokens_system_update ON app.refresh_tokens IS
'Allows app_system to update refresh tokens for revocation or rotation.';

