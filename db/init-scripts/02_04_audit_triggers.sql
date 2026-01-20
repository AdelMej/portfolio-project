\c audit

-- ------------------------------------------------------------------
-- Triggers: audit.events
--
-- Purpose:
-- - Enforce immutability of audit events
-- - Ensure append-only semantics
--
-- Guarantees:
-- - INSERT only
-- - No updates or deletes allowed
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: enforce append-only on audit.events
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION audit.tg_events_immutable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'audit.events is append-only; updates and deletes are forbidden';
END;
$$;

COMMENT ON FUNCTION audit.tg_events_immutable() IS
'Prevents UPDATE and DELETE on audit.events to enforce append-only semantics';

-- ------------------------------------------------------------------
-- Trigger: prevent updates
-- ------------------------------------------------------------------
CREATE TRIGGER trg_events_no_update
BEFORE UPDATE ON audit.events
FOR EACH ROW
EXECUTE FUNCTION audit.tg_events_immutable();

COMMENT ON TRIGGER trg_events_no_update ON audit.events IS
'Prevents modification of audit.events rows; append-only enforcement';

-- ------------------------------------------------------------------
-- Trigger: prevent deletes
-- ------------------------------------------------------------------
CREATE TRIGGER trg_events_no_delete
BEFORE DELETE ON audit.events
FOR EACH ROW
EXECUTE FUNCTION audit.tg_events_immutable();

COMMENT ON TRIGGER trg_events_no_delete ON audit.events IS
'Prevents deletion of audit.events rows; append-only enforcement';
