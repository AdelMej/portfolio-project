-- ------------------------------------------------------------------
-- Privileges: app.payment_intents
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- app_user: read-only
--
-- Access is limited by RLS, so users only see their own payment intents.
-- Used for:
-- - User dashboards
-- - Viewing their own payment history
-- ---------------------------------------------------------------
GRANT SELECT ON app.payment_intents TO app_user;

-- ---------------------------------------------------------------
-- app_system: full write access
--
-- Can read, insert, and update all payment intents.
-- Used for:
-- - System operations (e.g., creating intents for new sessions)
-- - Syncing payments with external providers
-- - Administrative maintenance
-- ---------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE ON app.payment_intents TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------
COMMENT ON TABLE app.payment_intents IS
'Payment intents table. app_user has read-only access filtered by RLS. app_system can read, insert, and update all rows for system operations.';
