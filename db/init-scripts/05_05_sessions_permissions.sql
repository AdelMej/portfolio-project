\c app

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Capabilities (GRANTs):
-- - SELECT: read access to sessions
-- - INSERT / UPDATE: authority enforced via RLS policies
--
-- Scope (RLS):
-- - Constrained by policies like:
--   - sessions_select_all
--   - sessions_coach_insert
--   - sessions_coach_or_admin_update
-- ---------------------------------------------------------------

GRANT SELECT ON TABLE app.sessions TO app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.sessions IS
'Table representing application sessions.
app_user may read sessions and perform RLS-gated creation/updates.
System operations (app_system) are executed via SECURITY DEFINER functions; no direct table privileges are granted.
All access is fully constrained by RLS policies; no direct privilege bypass is possible.';