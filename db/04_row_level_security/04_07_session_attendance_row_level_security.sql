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
	app_fcn.is_admin()
);

COMMENT ON POLICY session_attendance_select ON app.session_attendance IS
'Allows admins to read all session attendance records.';