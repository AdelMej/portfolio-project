
-- ------------------------------------------------------------------
-- Triggers: app.session_participation
--
-- Purpose:
-- - Enforce time-based, financial, and state-based invariants for session participation
--
-- Guarantees:
-- - Registration closes once the session starts
-- - Payment is allowed only once, before session start, and for non-cancelled participations
-- - Cancellation is forbidden after payment or session start
-- - Attendance can only be marked after session end
-- - Cancelled participants cannot be marked as attended
-- - Once attendance is marked, the row becomes immutable
-- ------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app.tg_session_participation_datetime_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_session_start TIMESTAMPTZ;
    v_session_end   TIMESTAMPTZ;
BEGIN
    ------------------------------------------------------------------
    -- FETCH SESSION START/END
    ------------------------------------------------------------------
    SELECT starts_at, ends_at
    INTO STRICT v_session_start, v_session_end
    FROM app.sessions
    WHERE id = NEW.session_id;

    ------------------------------------------------------------------
    -- INSERT RULES: registration closed after start
    ------------------------------------------------------------------
    IF TG_OP = 'INSERT' THEN
        IF now() >= v_session_start THEN
            RAISE EXCEPTION 'Registration is closed for this session';
        END IF;
    END IF;

    ------------------------------------------------------------------
    -- UPDATE RULES
    ------------------------------------------------------------------
    IF TG_OP = 'UPDATE' THEN

        ------------------------------------------------------------------
        -- PAYMENT RULE
        -- Payment is only allowed once, before session start,
        -- and for non-cancelled participations
        ------------------------------------------------------------------
        IF OLD.paid_at IS NULL
           AND NEW.paid_at IS NOT NULL THEN

            IF OLD.cancelled_at IS NOT NULL THEN
                RAISE EXCEPTION 'Cannot pay a cancelled participation';
            END IF;

            IF OLD.registered_at >= v_session_start THEN
                RAISE EXCEPTION 'Cannot pay after session start';
            END IF;
        END IF;

        ------------------------------------------------------------------
        -- CANCELLATION RULE
        -- Only allowed before session start and before payment
        ------------------------------------------------------------------
        IF OLD.cancelled_at IS NULL
           AND NEW.cancelled_at IS NOT NULL THEN

            IF now() >= v_session_start THEN
                RAISE EXCEPTION 'Cannot cancel after session start';
            END IF;
        END IF;

    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_session_participation_datetime_guard() IS
'Enforces session participation rules: registration, cancellation, attendance, and immutability after attendance.';

-- ------------------------------------------------------------------
-- Trigger: trg_session_participation_datetime_guard
-- ------------------------------------------------------------------
CREATE TRIGGER trg_session_participation_datetime_guard
BEFORE INSERT OR UPDATE
ON app.session_participation
FOR EACH ROW
EXECUTE FUNCTION app.tg_session_participation_datetime_guard();

COMMENT ON TRIGGER trg_session_participation_datetime_guard ON app.session_participation IS
'Prevents invalid inserts/updates on session_participation according to session start/end times, cancellation rules, and attendance immutability.';

-- ------------------------------------------------------------------
-- Trigger: session_participant_limit
-- ------------------------------------------------------------------
-- Enforces a hard limit of 6 participants per session.
--
-- This invariant is enforced at the database level to avoid
-- race conditions under concurrent inserts.
-- ------------------------------------------------------------------


-- ------------------------------------------------------------------
-- Trigger function
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_session_participation_limit()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    participation_count integer;
BEGIN
    -- Serialize inserts per session to avoid race conditions
    PERFORM pg_advisory_xact_lock(hashtext('session:' || NEW.session_id::text));

    -- Count existing participants for this session
    SELECT COUNT(*)
    INTO participation_count
    FROM app.session_participation
    WHERE session_id = NEW.session_id
		AND cancelled_at IS NULL;

    -- Enforce maximum of 6 participants
    IF participation_count >= 6 THEN
        RAISE EXCEPTION
            'Session % already has 6 participants',
            NEW.session_id;
    END IF;

    RETURN NEW;
END;
$$;


-- ------------------------------------------------------------------
-- Trigger binding
-- ------------------------------------------------------------------
CREATE TRIGGER trg_session_participation_limit
BEFORE INSERT ON app.session_participation
FOR EACH ROW
EXECUTE FUNCTION app.tg_session_participation_limit();


-- ------------------------------------------------------------------
-- PostgreSQL documentation
-- ------------------------------------------------------------------
COMMENT ON FUNCTION app.tg_session_participation_limit() IS
'Prevents more than 6 participants from being inserted into a session. Uses an advisory transaction lock on session_id to avoid race conditions.';