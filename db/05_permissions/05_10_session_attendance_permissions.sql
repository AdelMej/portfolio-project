-- ------------------------------------------------------------------
-- Privileges: app.session_attendance
--
-- Purpose:
-- - Grant access according to role responsibilities
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: coach can insert attendance
-- ------------------------------------------------------------------
GRANT SELECT, INSERT ON TABLE app.session_attendance TO app_user;

COMMENT ON TABLE app.session_attendance IS
'Coaches (app_user) can insert attendance records for their sessions only.';

-- ------------------------------------------------------------------
-- app_system: read-only for metrics, exports, and audits
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.session_attendance TO app_system;

COMMENT ON TABLE app.session_attendance IS
'System role (app_system) can read attendance records for reporting, metrics, and background jobs.';

-- ------------------------------------------------------------------
-- Remove default access
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE app.session_attendance FROM app_user;
REVOKE ALL ON TABLE app.session_attendance FROM app_system;

COMMENT ON TABLE app.session_attendance IS
'All other privileges are revoked; access is controlled via explicit grants above.';
