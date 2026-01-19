\c app

-- ------------------------------------------------------------------
-- Privileges: app.user_profiles
--
-- Access model:
-- - app_user   : read profiles (RLS-scoped) and update own profile
-- - app_system : create profiles (signup, sync, admin tooling)
--
-- Notes:
-- - DELETE is intentionally forbidden (soft-delete model)
-- - Row visibility and write scope are enforced via RLS policies
-- ------------------------------------------------------------------

-- app_user: read profiles and update own profile (RLS enforced)
GRANT SELECT, UPDATE ON TABLE app.user_profiles TO app_user;

-- app_system: responsible for profile creation
GRANT INSERT ON TABLE app.user_profiles TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.user_profiles IS
'User profile table. Access is governed by RLS; DELETE is intentionally forbidden. 
Users may read visible profiles and update their own. 
System role is responsible for profile creation.';
