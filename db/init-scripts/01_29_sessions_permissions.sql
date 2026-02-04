\c app

-- ------------------------------------------------------------------
-- Privileges: app.sessions
--
-- Purpose:
-- - Allow application users to interact with sessions
-- - Delegate all authority and scope enforcement to RLS
--
-- Guarantees:
-- - app_user privileges are intentionally broad
-- - All access (read/write) is constrained by RLS policies
-- - No direct privilege-based bypass is possible
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Application user access
--
-- Used by:
-- - session browsing
-- - session creation (coach-owned)
-- - session updates (coach or admin)
-- ------------------------------------------------------------------

GRANT SELECT, INSERT, UPDATE ON app.sessions TO app_user;
GRANT SELECT, UPDATE ON app.sessions TO app_system;