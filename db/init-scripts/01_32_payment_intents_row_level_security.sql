\c app

-- ------------------------------------------------------------------
-- Row Level Security: app.payment_intents
--
-- Visibility model:
-- - App-level admins see all
-- - Users see their own payment intents
-- - Only system role can insert or update
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.payment_intents ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.payment_intents FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: payment_intents_read
--
-- Who can SELECT payment intents:
-- 1. Owner (user_id = current user)
-- 2. App-level admin
-- ------------------------------------------------------------------
CREATE POLICY payment_intents_read
ON app.payment_intents
FOR SELECT
USING (
    user_id = current_setting('app.current_user_id')::uuid
    OR EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY payment_intents_read ON app.payment_intents IS
'Allows owners to read their own payment intents and admins to read all records.';

-- ------------------------------------------------------------------
-- Policy: payment_intents_system_insert
--
-- Only system role can create payment intents
-- (webhooks, cron, internal actions)
-- ------------------------------------------------------------------
CREATE POLICY payment_intents_system_insert
ON app.payment_intents
FOR INSERT
TO app_system
WITH CHECK (TRUE);

COMMENT ON POLICY payment_intents_system_insert ON app.payment_intents IS
'Restricts insertion of payment intents to the system role only.';

-- ------------------------------------------------------------------
-- Policy: payment_intents_system_update
--
-- Only system role can update payment intents
-- ------------------------------------------------------------------
CREATE POLICY payment_intents_system_update
ON app.payment_intents
FOR UPDATE
TO app_system
USING (TRUE)
WITH CHECK (TRUE);

COMMENT ON POLICY payment_intents_system_update ON app.payment_intents IS
'Restricts updates on payment intents to the system role only.';
