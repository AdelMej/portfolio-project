\c app

-- ------------------------------------------------------------------
-- Permissions: app.roles
--
-- Overview:
-- - Table exposes role metadata used for authorization and RLS policies
-- - GRANTs define *capabilities* (what a role may attempt)
-- - Scope is controlled via RLS joins and functions
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Capabilities (GRANTs):
-- - SELECT: read-only access for RLS policy joins and permission checks
--
-- Scope:
-- - Table is static reference data; no mutation allowed
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.roles TO app_user;

-- ---------------------------------------------------------------
-- Role: app_system
--
-- Purpose:
-- - Backend system operations
--
-- Capabilities (GRANTs):
-- - SELECT: read-only access for permission checks and system workflows
--
-- Scope:
-- - Table is static reference data; no mutation allowed
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.roles TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.roles IS
'Static role reference table. Read-only for all application roles; used exclusively by RLS policies and authorization logic. Mutations are admin-only and handled out-of-band.';
