\c app

-- ------------------------------------------------------------------
-- Permissions: app.users
--
-- Note:
-- - Row Level Security (RLS) is enforced
-- - GRANTs define *capability*
-- - RLS defines *scope*
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Allowed:
-- - SELECT: read own user record
-- - UPDATE: update own profile fields
--
-- Scope:
-- - Fully restricted by RLS
-- ---------------------------------------------------------------

GRANT SELECT, UPDATE ON TABLE app.users TO app_user;

COMMENT ON TABLE app.users IS
'User accounts table. Access controlled via RLS. app_user may read/update own record only.';

COMMENT ON ROLE app_user IS
'Runtime application role. Reads and updates own user record via RLS-controlled access.';

-- ---------------------------------------------------------------
-- Role: app_system
--
-- Purpose:
-- - Backend system operations
-- - Signup flows
-- - Webhooks / identity sync
--
-- Allowed:
-- - SELECT: read users
-- - INSERT: create users
-- - UPDATE: system-managed updates
--
-- Scope:
-- - Still constrained by RLS
-- ---------------------------------------------------------------

GRANT SELECT, INSERT, UPDATE ON TABLE app.users TO app_system;

COMMENT ON ROLE app_system IS
'System-level application role used for backend processes such as signup, sync, and admin workflows. Subject to RLS.';
