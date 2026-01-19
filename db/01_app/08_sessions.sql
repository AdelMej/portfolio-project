-- ------------------------------------------------------------------
-- Enum: app.session_status
--
-- Defines the lifecycle state of a session.
-- ------------------------------------------------------------------

CREATE TYPE app.session_status AS ENUM (
    'scheduled',
    'cancelled',
    'completed'
);

COMMENT ON TYPE app.session_status IS
'Lifecycle status of a session.';

-- ------------------------------------------------------------------
-- Table: app.sessions
--
-- Purpose:
-- - Represents a scheduled coaching session
-- - Defines immutable time boundaries and lifecycle state
--
-- Used for:
-- - session registration
-- - attendance tracking
-- - billing / credit usage
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.sessions (
    -- Unique session identifier
    id UUID PRIMARY KEY,

    -- Coach hosting the session
    coach_id UUID NOT NULL,

    -- Public session title
    title VARCHAR(128) NOT NULL,

    -- Session start time (UTC)
    starts_at TIMESTAMPTZ NOT NULL,

    -- Session end time (UTC)
    ends_at TIMESTAMPTZ NOT NULL,

    -- Session lifecycle status
    status app.session_status NOT NULL DEFAULT 'scheduled',
    
    -- Audit fields
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_sessions_coach_id
        FOREIGN KEY (coach_id)
        REFERENCES app.users(id)
        ON DELETE CASCADE,
        
    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- End must be strictly after start
    CONSTRAINT chk_sessions_time_valid
        CHECK (ends_at > starts_at),

    -- Prevent empty titles
    CONSTRAINT chk_sessions_title_not_empty
        CHECK (title <> '')
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.sessions IS
'Represents a scheduled coaching session with defined time bounds and lifecycle state.';

COMMENT ON COLUMN app.sessions.id IS
'Primary identifier for the session.';

COMMENT ON COLUMN app.sessions.coach_id IS
'User acting as the coach hosting the session.';

COMMENT ON COLUMN app.sessions.title IS
'Human-readable title of the session.';

COMMENT ON COLUMN app.sessions.starts_at IS
'Scheduled start timestamp of the session (UTC).';

COMMENT ON COLUMN app.sessions.ends_at IS
'Scheduled end timestamp of the session (UTC).';

COMMENT ON COLUMN app.sessions.status IS
'Lifecycle status of the session (scheduled, cancelled, completed).';

COMMENT ON COLUMN app.sessions.created_at IS
'Timestamp when the session record was created (UTC).';

COMMENT ON COLUMN app.sessions.updated_at IS
'Timestamp when the session record was last updated (UTC).';

