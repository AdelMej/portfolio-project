\c app

-- ------------------------------------------------------------------
-- Table: audit.events
-- ------------------------------------------------------------------
-- Purpose:
-- - Record append-only audit events for the system
-- - Capture all critical actions for compliance, debugging, and analytics
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS audit.events (
    -- ------------------------------------------------------------------
    -- Primary key
    -- ------------------------------------------------------------------
    id BIGINT GENERATED ALWAYS AS IDENTITY,

    -- ------------------------------------------------------------------
    -- Event timestamp
    -- ------------------------------------------------------------------
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- ------------------------------------------------------------------
    -- Actor information
    -- ------------------------------------------------------------------
    actor_type TEXT NOT NULL,    -- 'stripe', 'user', 'system'
    actor_id   UUID NULL,        -- nullable for system events

    -- ------------------------------------------------------------------
    -- Event details
    -- ------------------------------------------------------------------
    event_type TEXT NOT NULL,    -- SESSION_CREATED, USER_DISABLED, etc.
    target_id  UUID NULL,        -- optional reference to the affected object

    -- ------------------------------------------------------------------
    -- Additional metadata
    -- ------------------------------------------------------------------
    metadata JSONB NOT NULL DEFAULT '{}'
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------
COMMENT ON TABLE audit.events IS
'Append-only audit log of system events for compliance, debugging, and analytics.';

COMMENT ON COLUMN audit.events.id IS
'Primary key for audit events.';

COMMENT ON COLUMN audit.events.occurred_at IS
'Timestamp when the event occurred (UTC).';

COMMENT ON COLUMN audit.events.actor_type IS
'Type of actor triggering the event (e.g., stripe, user, system).';

COMMENT ON COLUMN audit.events.actor_id IS
'Optional UUID of the actor; null if system-generated.';

COMMENT ON COLUMN audit.events.event_type IS
'Type of event (e.g., SESSION_CREATED, USER_DISABLED).';

COMMENT ON COLUMN audit.events.target_id IS
'Optional reference to the affected entity.';

COMMENT ON COLUMN audit.events.metadata IS
'JSONB containing any additional data relevant to the event.';
