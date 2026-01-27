-- ------------------------------------------------------------------
-- Privileges: app.payment
--
-- Purpose:
-- - Grant access according to role responsibilities
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: read-only
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.payment TO app_user;

COMMENT ON TABLE app.payment IS
'Regular users (app_user) may read their own payments (RLS enforced).';

-- ------------------------------------------------------------------
-- app_admin: database administrator
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.payment TO app_admin;

COMMENT ON TABLE app.payment IS
'Database administrators (app_admin) may read all payments (RLS allows full visibility).';

-- ------------------------------------------------------------------
-- app_system: insert only (creates new payments)
-- ------------------------------------------------------------------
GRANT INSERT ON TABLE app.payment TO app_system;

COMMENT ON TABLE app.payment IS
'System automation (app_system) may create new payment records only. No update or delete allowed.';
