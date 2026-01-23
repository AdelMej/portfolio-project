 \c app

-- ------------------------------------------------------------------
-- Table: app.session_participation
--
-- Purpose:
-- - Represents user registration for a session
-- - Acts as the source of truth for participation intent
--
-- Used for:
-- - enforcing attendance eligibility
-- - cancellation tracking
-- - billing / credit validation
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.session_participation (
    -- Unique participation identifier
    id UUID PRIMARY KEY,

    -- Target session
    session_id UUID NOT NULL,

    -- Participating user
    user_id UUID NOT NULL,

    -- Paid timestamp
    paid_at TIMESTAMPTZ NULL,
    
    -- Registration timestamp
    registered_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Cancellation timestamp (NULL = active)
    cancelled_at TIMESTAMPTZ NULL,

    -- ------------------------------------------------------------------
    -- Invariants
    -- ------------------------------------------------------------------

    -- Prevent double registration for the same session
    CONSTRAINT uq_session_participation_user_session
        UNIQUE (session_id, user_id),

    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    CONSTRAINT fk_session_participants_session_id
        FOREIGN KEY (session_id)
        REFERENCES app.sessions(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_session_participants_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.session_participation IS
'Represents user registration intent for a session. Source of truth for who is allowed to attend.';

COMMENT ON COLUMN app.session_participation.id IS
'Primary identifier for the participation record.';

COMMENT ON COLUMN app.session_participation.session_id IS
'Session the user is registering for.';

COMMENT ON COLUMN app.session_participation.user_id IS
'User registering for the session.';

COMMENT ON COLUMN app.session_participation.registered_at IS
'Timestamp when the user registered for the session.';

COMMENT ON COLUMN app.session_participation.cancelled_at IS
'Timestamp when the participation was cancelled. NULL means the registration is active.';

COMMENT ON COLUMN app.session_participation.paid_at IS
'Timestamp when the participation was successfully paid. NULL means the registration is not yet financially confirmed.';
