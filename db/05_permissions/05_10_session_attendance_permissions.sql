-- ------------------------------------------------------------------
-- Privileges: app.session_attendance
--
-- Purpose:
-- - Store authoritative attendance records for sessions
-- - Allow administrative visibility into attendance data
-- - Delegate all authority and scope enforcement to RLS
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: read access (RLS-scoped)
--
-- Notes:
-- - app_user has SELECT privilege
-- - Actual visibility is restricted to admins by RLS
-- - Non-admin users will see zero rows
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.session_attendance
TO app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.session_attendance IS
'Session attendance records. SELECT is granted to app_user, but visibility is fully restricted by RLS to administrative roles only. 
Regular users and coaches cannot observe or mutate attendance data. 
All inserts and updates are performed by system-owned backend logic.';
