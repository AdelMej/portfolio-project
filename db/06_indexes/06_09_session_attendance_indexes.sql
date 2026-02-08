-- ------------------------------------------------------------------
-- Indexes: app.session_attendance
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Lookup all attendance records for a specific session
-- Used by:
-- - Coach dashboards
-- - Session reports
-- ---------------------------------------------------------------
CREATE INDEX idx_session_attendance_session_id
ON app.session_attendance (session_id);

COMMENT ON INDEX app.idx_session_attendance_session_id IS
'Optimizes queries filtering by session_id to retrieve all attendance records for a session.';

-- ---------------------------------------------------------------
-- Lookup attendance records for a specific user
-- Used by:
-- - User dashboards
-- - Historical attendance queries
-- ---------------------------------------------------------------
CREATE INDEX idx_session_attendance_user_id
ON app.session_attendance (user_id);

COMMENT ON INDEX app.idx_session_attendance_user_id IS
'Speeds up queries filtering by user_id to find all sessions a user attended.';

-- ---------------------------------------------------------------
-- Composite lookup by session and user
-- Ensures uniqueness already via PK but improves certain query plans
-- Used by:
-- - Quick existence checks
-- - RLS joins with session_participation
-- ---------------------------------------------------------------
CREATE INDEX idx_session_attendance_session_user
ON app.session_attendance (session_id, user_id);

COMMENT ON INDEX app.idx_session_attendance_session_user IS
'Enhances performance of queries filtering on both session_id and user_id.';

-- ---------------------------------------------------------------
-- Fast lookup for attended session records
-- Used by:
-- - Analytics / reports on completed sessions
-- ---------------------------------------------------------------
CREATE INDEX idx_session_attendance_attended
ON app.session_attendance (attended)
WHERE attended = true;

COMMENT ON INDEX app.idx_session_attendance_attended IS
'Speeds up queries retrieving attended session records for reporting and metrics.';