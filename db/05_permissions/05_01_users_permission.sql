-- ------------------------------------------------------------------
-- Permissions: app.users
--
-- Overview:
-- - Row Level Security (RLS) is enforced to control *scope* of access.
-- - GRANTs define *capabilities* (what a role may attempt).
-- - RLS + functions determine the actual allowed operations.
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users.
--
-- Capabilities (GRANTs):
-- - SELECT: read own user record
-- - UPDATE: update own profile fields
--
-- Scope (RLS):
-- - Fully restricted by RLS policies such as:
--   - users_select_self_or_admin
--   - users_self_update
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.users TO app_user;

COMMENT ON TABLE app.users IS
'User accounts table. Access controlled via RLS. app_user may read/update their own record only.';

-- ---------------------------------------------------------------
-- Role: app_system
--
-- Purpose:
-- - Backend system operations: signup flows, webhooks, identity sync, admin workflows.
--
-- Capabilities (GRANTs):
-- - SELECT only on table
-- - All inserts/updates/deletes are performed via SECURITY DEFINER functions
--
-- Scope (RLS):
-- - app_system still subject to RLS for direct table access
-- - Privileged operations are done via functions (functions bypass table GRANT restrictions)
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.users TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON ROLE app_system IS
'System-level role for backend processes such as signup, sync, and admin workflows. Direct table access is read-only; all other operations performed via SECURITY DEFINER functions.';