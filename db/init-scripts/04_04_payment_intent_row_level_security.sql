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
    app_fcn.is_self(user_id)
    OR app_fcn.is_admin()
);

COMMENT ON POLICY payment_intents_read ON app.payment_intents IS
'Allows owners to read their own payment intents and admins to read all records.';
