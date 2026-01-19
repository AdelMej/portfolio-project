-- ------------------------------------------------------------------
-- Privileges: app.user_roles
--
-- Purpose:
-- - Allow users to read role assignments (RLS-scoped)
-- - Allow controlled role management via RLS
-- - Support system-level automation
--
-- Guarantees:
-- - app_user visibility is fully restricted by RLS
-- - Admin actions (insert/delete) are enforced at the policy level
-- - app_system bypasses user intent but still respects schema rules
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Read access
--
-- Used by:
-- - permission checks
-- - role-aware queries
-- - RLS joins
-- ------------------------------------------------------------------

GRANT SELECT ON app.user_roles TO app_user;

-- ------------------------------------------------------------------
-- Role management (RLS-gated)
--
-- app_user:
-- - insert/delete allowed
-- - actual authority enforced by RLS policies
--
-- app_system:
-- - used for automation, provisioning, sync jobs
-- ------------------------------------------------------------------

GRANT INSERT, DELETE ON app.user_roles TO app_user;
GRANT SELECT, INSERT, DELETE ON app.user_roles TO app_system;
