-- ------------------------------------------------------------------
-- Triggers: app.sessions
--
-- Purpose:
-- - Enforce immutability rules for session identity
-- - Maintain audit consistency (updated_at)
-- - Enforce session time and lifecycle rules
--
-- Guarantees:
-- - id and coach_id are immutable
-- - start/end times cannot be changed after session start
-- - status transitions are strictly controlled
-- - updated_at is always refreshed on UPDATE
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: auto-update updated_at
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_sessions_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_sessions_set_updated_at() IS
'Automatically updates updated_at timestamp on every session update.';

-- ------------------------------------------------------------------
-- Trigger: set updated_at on update
-- ------------------------------------------------------------------

CREATE TRIGGER trg_10_sessions_set_updated_at
BEFORE UPDATE ON app.sessions
FOR EACH ROW
EXECUTE FUNCTION app.tg_sessions_set_updated_at();

COMMENT ON TRIGGER trg_10_sessions_set_updated_at ON app.sessions IS
'Ensures updated_at reflects the last modification time.';

-- ------------------------------------------------------------------
-- Function: prevent mutation of id and coach_id
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_sessions_immutable_identity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.id <> OLD.id THEN
        RAISE EXCEPTION 'sessions.id is immutable';
    END IF;

    IF NEW.coach_id <> OLD.coach_id THEN
        RAISE EXCEPTION 'sessions.coach_id is immutable';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_sessions_immutable_identity() IS
'Prevents any changes to session primary key or coach assignment.';

-- ------------------------------------------------------------------
-- Trigger: enforce immutable identity
-- ------------------------------------------------------------------

CREATE TRIGGER trg_20_sessions_immutable_identity
BEFORE UPDATE ON app.sessions
FOR EACH ROW
EXECUTE FUNCTION app.tg_sessions_immutable_identity();

COMMENT ON TRIGGER trg_20_sessions_immutable_identity ON app.sessions IS
'Blocks attempts to change id or coach_id after session creation.';

-- ------------------------------------------------------------------
-- Function: lock session times after start
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_sessions_time_lock()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF clock_timestamp() >= OLD.starts_at THEN
        IF NEW.starts_at <> OLD.starts_at
           OR NEW.ends_at <> OLD.ends_at THEN
            RAISE EXCEPTION
                'Cannot modify session time after it has started';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_sessions_time_lock() IS
'Prevents modification of session start and end times after the session has begun. Uses real current time (clock_timestamp()).';

-- ------------------------------------------------------------------
-- Trigger: enforce time immutability
-- ------------------------------------------------------------------

CREATE TRIGGER trg_30_sessions_time_lock
BEFORE UPDATE ON app.sessions
FOR EACH ROW
EXECUTE FUNCTION app.tg_sessions_time_lock();

COMMENT ON TRIGGER trg_30_sessions_time_lock ON app.sessions IS
'Blocks updates to starts_at or ends_at after session start.';

-- ------------------------------------------------------------------
-- Function: validate status transitions
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_sessions_validate_status_transition()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.status <> OLD.status THEN

        -- only scheduled → cancelled/completed allowed
        IF OLD.status = 'scheduled'
           AND NEW.status IN ('cancelled', 'completed') THEN
            RETURN NEW;
        END IF;

        RAISE EXCEPTION
            'Invalid session status transition: % → %',
            OLD.status, NEW.status;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_sessions_validate_status_transition() IS
'Ensures sessions can only move from scheduled → cancelled or completed. Prevents other transitions.';

-- ------------------------------------------------------------------
-- Trigger: enforce status transitions
-- ------------------------------------------------------------------

CREATE TRIGGER trg_40_sessions_validate_status_transition
BEFORE UPDATE ON app.sessions
FOR EACH ROW
EXECUTE FUNCTION app.tg_sessions_validate_status_transition();

COMMENT ON TRIGGER trg_40_sessions_validate_status_transition ON app.sessions IS
'Validates session status changes and prevents invalid transitions.';
