-- ------------------------------------------------------------------
-- Table: app.session_attendance
--
-- Purpose:
-- - Records actual attendance outcome for a session
-- - Represents the final, authoritative attendance state
--
-- Used for:
-- - attendance lists
-- - reporting / exports
-- - compliance / audits
--
-- This table is intentionally write-once.
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.session_attendance (
    -- Unique attendance identifier
    id UUID PRIMARY KEY,

    -- Target session
    session_id UUID NOT NULL,

    -- Attending user
    user_id UUID NOT NULL,

    -- Attendance outcome
    -- TRUE  = attended
    -- FALSE = explicitly marked as absent
    attended BOOLEAN NOT NULL,

    -- Audit fields
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    recorded_by UUID NOT NULL,

    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- One attendance record per user per session
    CONSTRAINT uq_session_attendance_user_session
        UNIQUE (session_id, user_id),

    -- Attendance must correspond to an existing participation
    CONSTRAINT fk_attendance_participation
        FOREIGN KEY (session_id, user_id)
        REFERENCES app.session_participation(session_id, user_id)
        ON DELETE RESTRICT,

    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_attendance_session
        FOREIGN KEY (session_id)
        REFERENCES app.sessions(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_attendance_user
        FOREIGN KEY (user_id)
        REFERENCES app.users(id)
        ON DELETE RESTRICT
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.session_attendance IS
'Final attendance records for sessions. Write-once table representing ground truth of attendance outcomes.';

COMMENT ON COLUMN app.session_attendance.id IS
'Primary identifier for the attendance record.';

COMMENT ON COLUMN app.session_attendance.session_id IS
'Session for which attendance is being recorded.';

COMMENT ON COLUMN app.session_attendance.user_id IS
'User whose attendance is being recorded.';

COMMENT ON COLUMN app.session_attendance.attended IS
'Attendance outcome. TRUE means the user attended; FALSE means explicitly marked absent.';

COMMENT ON COLUMN app.session_attendance.recorded_at IS
'Timestamp when the attendance was recorded.';

COMMENT ON COLUMN app.session_attendance.recorded_by IS
'User (typically coach or system) who recorded the attendance.';
