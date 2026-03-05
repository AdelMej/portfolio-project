\c app

-- ------------------------------------------------------------------
-- Permissions: app.user_roles
--
-- Overview:
-- - Controls user ↔ role assignments
-- - GRANTs define *capabilities* (what actions a role may attempt)
-- - RLS policies enforce *scope* and authority
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated users
--
-- Capabilities (GRANTs):
-- - SELECT: read own role assignments (RLS-scoped)
-- - INSERT / DELETE: allowed but actual authority is enforced by RLS policies
--
-- Scope (RLS):
-- - Fully restricted by RLS policies such as:
--   - user_roles_visible
--   - user_roles_admin_or_system_delete
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.user_roles TO app_user;

-- ---------------------------------------------------------------
-- Role: app_system
--
-- Purpose:
-- - Backend automation, provisioning, and sync jobs
--
-- Capabilities (GRANTs):
-- - SELECT: read access to all role assignments
-- - All inserts/deletes performed via SECURITY DEFINER functions if needed
--
-- Scope (RLS):
-- - Table access subject to RLS for direct queries
-- - Privileged operations handled through functions
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.user_roles TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.user_roles IS
'Table mapping users to roles. 
app_user may read their own assignments and perform RLS-gated inserts/deletes.
Admin actions are enforced at the policy level.
app_system may perform automation and system-level operations via SECURITY DEFINER functions.';
