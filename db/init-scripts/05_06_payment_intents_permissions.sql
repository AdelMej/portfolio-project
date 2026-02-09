\c app

-- ------------------------------------------------------------------
-- Permissions: app.payment_intents
--
-- Overview:
-- - Stores payment intent records
-- - GRANTs define *capabilities* (what a role may attempt)
-- - RLS policies enforce *scope* and authority
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Capabilities (GRANTs):
-- - SELECT: read-only access to payment intents
--
-- Scope (RLS):
-- - Fully constrained by RLS policies such as:
--   - payment_intents_read
-- - Users only see their own payment intents
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.payment_intents TO app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.payment_intents IS
'Payment intents table. 
app_user has read-only access filtered by RLS policies. 
System operations are executed via SECURITY DEFINER functions; no direct table privileges are granted.';
