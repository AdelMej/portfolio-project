\c app

-- ------------------------------------------------------------------
-- Row Level Security: app.session_attendance
--
-- Visibility model:
-- - Only system inserts attendance
-- - Admins can read attendance
-- - Coaches and users do not access this table directly
-- ------------------------------------------------------------------

ALTER TABLE app.session_attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.session_attendance FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: session_attendance_select
--
-- Admins may read attendance
-- ------------------------------------------------------------------
CREATE POLICY session_attendance_select
ON app.session_attendance
FOR SELECT
USING (
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY session_attendance_select ON app.session_attendance IS
'Allows admins to read all session attendance records.';

-- ------------------------------------------------------------------
-- Policy: session_attendance_system_insert
--
-- System inserts attendance based on participation mapping
-- ------------------------------------------------------------------
CREATE POLICY session_attendance_system_insert
ON app.session_attendance
FOR INSERT
TO app_system
WITH CHECK (TRUE);

COMMENT ON POLICY session_attendance_system_insert ON app.session_attendance IS
'System inserts attendance rows; ensures consistency and immutable attendance.';

-- ------------------------------------------------------------------
-- Privileges: app.session_attendance
-- ------------------------------------------------------------------

-- app_user: no direct access
REVOKE ALL ON TABLE app.session_attendance FROM app_user;

COMMENT ON TABLE app.session_attendance IS
'Users cannot access attendance directly; they see participation only.';

-- app_system: insert-only
GRANT INSERT ON TABLE app.session_attendance TO app_system;

COMMENT ON TABLE app.session_attendance IS
'System inserts attendance rows derived from session_participation; no updates allowed.';

-- app_admin: read-only
GRANT SELECT ON TABLE app.session_attendance TO app_admin;

COMMENT ON TABLE app.session_attendance IS
'Admins can read attendance records for auditing and reporting.';
