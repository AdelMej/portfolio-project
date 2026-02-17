\c app

-- ------------------------------------------------------------------
-- Triggers: app.session_attendance
--
-- Purpose:
-- - Enforce business invariants for session attendance
-- - Prevent invalid or unauthorized attendance recording
--
-- Guarantees:
-- - Attendance is INSERT-ONLY
-- - Cannot record attendance before session starts
-- - User must be a registered, non-cancelled participant
-- - Session reference must be valid
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: session attendance guard
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_session_attendance_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_starts_at TIMESTAMPTZ;
BEGIN
    ----------------------------------------------------------------------
    -- IMMUTABILITY
    ----------------------------------------------------------------------
    IF TG_OP <> 'INSERT' THEN
        RAISE EXCEPTION 'Session attendance is immutable';
    END IF;

    ----------------------------------------------------------------------
    -- SESSION VALIDATION
    ----------------------------------------------------------------------
    SELECT s.starts_at
    INTO v_starts_at
    FROM app.sessions s
    WHERE s.id = NEW.session_id;

    IF v_starts_at IS NULL THEN
        RAISE EXCEPTION 'Invalid session reference';
    END IF;

    ----------------------------------------------------------------------
    -- TEMPORAL RULE
    ----------------------------------------------------------------------
    IF now() < v_starts_at THEN
        RAISE EXCEPTION 'Cannot mark attendance before session start';
    END IF;

    ----------------------------------------------------------------------
    -- PARTICIPATION INVARIANT
    ----------------------------------------------------------------------
    IF NOT EXISTS (
        SELECT 1
        FROM app.session_participation sp
        WHERE sp.session_id = NEW.session_id
          AND sp.user_id = NEW.user_id
          AND sp.cancelled_at IS NULL
    ) THEN
        RAISE EXCEPTION 'User is not an active participant for this session';
    END IF;

    ----------------------------------------------------------------------
    -- All invariants satisfied
    ----------------------------------------------------------------------
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_session_attendance_guard() IS
'Enforces append-only session attendance: ensures valid session, temporal constraints, and active participation.';

-- ------------------------------------------------------------------
-- Trigger: enforce session attendance guard
-- ------------------------------------------------------------------
CREATE TRIGGER trg_session_attendance_guard
BEFORE INSERT
ON app.session_attendance
FOR EACH ROW
EXECUTE FUNCTION app.tg_session_attendance_guard();

COMMENT ON TRIGGER trg_session_attendance_guard ON app.session_attendance IS
'Prevents invalid inserts/updates/deletes on session_attendance according to session timing and participation rules.';

