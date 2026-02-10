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
TO app_user
USING (
    app_fcn.is_self(user_id)
    OR app_fcn.is_admin()
);

COMMENT ON POLICY refresh_tokens_select_user_admin ON app.refresh_tokens IS
'Allows users to read their own refresh tokens and admins to read all tokens.';
