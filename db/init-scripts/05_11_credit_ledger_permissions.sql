\c app

-- ------------------------------------------------------------------
-- Permissions: app.credit_ledger
--
-- Purpose:
-- - Store immutable credit ledger entries
-- - Allow users to view their own credit history
-- - Allow admins to audit all ledger activity
--
-- Design notes:
-- - Ledger is append-only (enforced elsewhere)
-- - All mutations are performed by system-owned logic
-- - Row visibility is enforced exclusively via RLS
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Privilege cleanup
--
-- Notes:
-- - Explicitly revoke all privileges before re-granting
-- - Ensures a known, auditable baseline
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE app.credit_ledger FROM app_user;
REVOKE ALL ON TABLE app.credit_ledger FROM app_admin;
REVOKE ALL ON TABLE app.credit_ledger FROM app_system;

-- ------------------------------------------------------------------
-- app_user: read-only (RLS-scoped)
--
-- Notes:
-- - Users may read their own ledger entries only
-- - RLS enforces row-level ownership
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.credit_ledger
TO app_user;

-- ------------------------------------------------------------------
-- app_admin: read-only
--
-- Notes:
-- - Admins may read all ledger entries
-- - Used for auditing, reconciliation, and support
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.credit_ledger
TO app_admin;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.credit_ledger IS
'Immutable credit ledger table.
SELECT is granted to app_user and app_admin, while all row-level visibility is enforced by RLS.
Users may view their own entries; admins may audit all entries.
All inserts are performed by system-owned backend logic.';