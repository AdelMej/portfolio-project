-- ------------------------------------------------------------------
-- Privileges: app.payment
--
-- Purpose:
-- - Store immutable payment records
-- - Allow users to view their own payments
-- - Allow admins to audit all payments
--
-- Design notes:
-- - Table is append-only
-- - Updates and deletes are intentionally forbidden
-- - All inserts are performed by backend system logic
-- - Row visibility is enforced exclusively via RLS
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Privilege cleanup
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE app.payment FROM app_user;
REVOKE ALL ON TABLE app.payment FROM app_admin;
REVOKE ALL ON TABLE app.payment FROM app_system;

-- ------------------------------------------------------------------
-- app_user: read-only (RLS-scoped)
--
-- Notes:
-- - Users may read their own payment records only
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.payment
TO app_user;

-- ------------------------------------------------------------------
-- app_admin: read-only (RLS-scoped)
--
-- Notes:
-- - Admins may audit all payment records
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.payment
TO app_admin;

-- ------------------------------------------------------------------
-- app_system: insert-only
--
-- Notes:
-- - Used by webhooks and backend automation
-- - No update or delete allowed
-- ------------------------------------------------------------------
GRANT INSERT
ON TABLE app.payment
TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.payment IS
'Immutable payment records table.
SELECT is granted to app_user and app_admin; INSERT is granted to app_system.
All row-level visibility is enforced by RLS.
Updates and deletes are intentionally forbidden.';
