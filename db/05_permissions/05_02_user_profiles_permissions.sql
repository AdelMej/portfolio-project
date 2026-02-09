-- ------------------------------------------------------------------
-- Permissions: app.user_profiles
--
-- Overview:
-- - Row Level Security (RLS) enforces *scope* of access.
-- - GRANTs define *capabilities* (what a role may attempt).
-- - RLS + functions determine the actual allowed operations.
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Capabilities (GRANTs):
-- - SELECT: read profiles (RLS-scoped)
-- - UPDATE: update own profile fields
--
-- Scope (RLS):
-- - Fully restricted by RLS policies such as:
--   - user_profiles_visible
--   - user_profiles_self_update
-- ---------------------------------------------------------------

GRANT SELECT, UPDATE ON TABLE app.user_profiles TO app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.user_profiles IS
'User profile table. Access controlled via RLS; DELETE is intentionally forbidden (soft-delete model). 
app_user may read visible profiles and update their own. 
app_system handles profile creation via SECURITY DEFINER functions.';
