\c app

-- ------------------------------------------------------------------
-- Privileges: app.roles
--
-- Purpose:
-- - Expose role metadata for authorization checks
-- - Used exclusively in RLS policies and permission joins
--
-- Design notes:
-- - roles table is static reference data
-- - No application role may INSERT / UPDATE / DELETE
-- - Mutations are admin-only and handled out-of-band
-- ------------------------------------------------------------------

-- app_user: read-only access (required for RLS joins)
GRANT SELECT ON TABLE app.roles TO app_user;

-- app_system: read-only access
GRANT SELECT ON TABLE app.roles TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.roles IS
'Static role reference table. Read-only for application roles; used by RLS and authorization logic.';
