-- ------------------------------------------------------------------
-- Privileges: app.session_participation
--
-- Purpose:
-- - Expose session participation data to end users
-- - Enforce read-only access for application users
-- - Delegate all mutations to system-owned logic
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: read-only access
--
-- Notes:
-- - app_user has SELECT access only
-- - Row visibility is strictly enforced by RLS
-- - Users cannot create, update, or cancel participation directly
-- - All lifecycle changes are performed by backend logic (app_system)
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.session_participation
TO app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.session_participation IS
'Session participation records. Application users (app_user) have read-only access scoped by RLS. 
All participation lifecycle operations (register, cancel, status changes) are performed exclusively by system-owned backend logic.';