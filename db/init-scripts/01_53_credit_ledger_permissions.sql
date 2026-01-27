\c app

-- ------------------------------------------------------------------
-- Privileges: app.credit_ledger
--
-- Purpose:
-- - Grant access according to role responsibilities
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Revoke all existing privileges
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE app.credit_ledger FROM app_user;
REVOKE ALL ON TABLE app.credit_ledger FROM app_admin;
REVOKE ALL ON TABLE app.credit_ledger FROM app_system;

COMMENT ON TABLE app.credit_ledger IS
'Initial cleanup of all privileges on credit_ledger before applying role-specific grants.';

-- ------------------------------------------------------------------
-- app_user: read-only
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.credit_ledger TO app_user;

COMMENT ON TABLE app.credit_ledger IS
'Regular users (app_user) may read their own ledger entries; RLS enforces row-level visibility.';

-- ------------------------------------------------------------------
-- app_admin: read-only
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.credit_ledger TO app_admin;

COMMENT ON TABLE app.credit_ledger IS
'Admin users (app_admin) may read all ledger entries for auditing and support purposes; RLS applies.';

-- ------------------------------------------------------------------
-- app_system: full write access
-- ------------------------------------------------------------------
GRANT SELECT, INSERT ON TABLE app.credit_ledger TO app_system;

COMMENT ON TABLE app.credit_ledger IS
'System role (app_system) may insert and read ledger entries; all updates are forbidden by RLS.';

