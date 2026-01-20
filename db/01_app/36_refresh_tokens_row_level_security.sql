-- ------------------------------------------------------------------
-- Row Level Security: app.refresh_tokens
--
-- Visibility and write model:
-- - Users can see only their own tokens
-- - App-level admins can see all tokens
-- - app_system can see all tokens and manage them
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.refresh_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.refresh_tokens FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_select
--
-- Who can SELECT tokens:
-- 1. Self
-- 2. App-level admins
-- 3. app_system
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_select
ON app.refresh_tokens
FOR SELECT
USING (
    ------------------------------------------------------------------
    -- 1. Self
    ------------------------------------------------------------------
    user_id = current_setting('app.current_user_id')::uuid

    OR

    ------------------------------------------------------------------
    -- 2. App-level admin
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )

    OR

    ------------------------------------------------------------------
    -- 3. app_system
    ------------------------------------------------------------------
    current_user = 'app_system'
);

COMMENT ON POLICY refresh_tokens_select ON app.refresh_tokens IS
'Controls visibility of refresh tokens: self, admin, or system process.';

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_system_insert
--
-- Only app_system may create tokens
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_system_insert
ON app.refresh_tokens
FOR INSERT
TO app_system
WITH CHECK (TRUE);

COMMENT ON POLICY refresh_tokens_system_insert ON app.refresh_tokens IS
'Restricts token creation to the system role.';

-- ------------------------------------------------------------------
-- Policy: refresh_tokens_system_update
--
-- Only app_system may update tokens (for revocation or replacement)
-- ------------------------------------------------------------------
CREATE POLICY refresh_tokens_system_update
ON app.refresh_tokens
FOR UPDATE
TO app_system
USING (TRUE)
WITH CHECK (TRUE);

COMMENT ON POLICY refresh_tokens_system_update ON app.refresh_tokens IS
'Allows app_system to update refresh tokens for revocation or replacement.';
