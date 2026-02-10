-- ------------------------------------------------------------------
-- Triggers: audit.events
--
-- Purpose:
-- - Enforce immutability of audit events
-- - Ensure database-controlled event timestamps
--
-- Design principles:
-- - Audit events are append-only historical facts
-- - Once written, events must never be modified or removed
-- - Triggers enforce structural guarantees only
--
-- Non-goals:
-- - Validate event payload correctness
-- - Enforce business invariants
--
-- Notes:
-- - Invalid or unexpected data may still be recorded intentionally
-- - Consumers are responsible for interpreting event semantics
-- ------------------------------------------------------------------


-- ------------------------------------------------------------------
-- Trigger function: prevent event mutation
--
-- Guarantees:
-- - UPDATE and DELETE operations are rejected
--
-- Rationale:
-- - Mutating audit events breaks forensic integrity
-- - Hard failure is preferred over silent corruption
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION audit.tg_prevent_event_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'Audit event records are immutable';
END;
$$;


-- ------------------------------------------------------------------
-- Trigger: block UPDATE / DELETE on audit.events
-- ------------------------------------------------------------------
CREATE TRIGGER trg_event_no_update
BEFORE UPDATE OR DELETE
ON audit.events
FOR EACH ROW
EXECUTE FUNCTION audit.tg_prevent_event_mutation();


-- ------------------------------------------------------------------
-- Trigger function: enforce occurred_at timestamp
--
-- Guarantees:
-- - occurred_at is always assigned by the database
-- - Client-supplied timestamps are ignored
--
-- Notes:
-- - occurred_at represents ingestion time
-- - External event times (e.g. Stripe event time) must be stored separately
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION audit.tg_enforce_event_occurred_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.occurred_at := now();
    RETURN NEW;
END;
$$;


-- ------------------------------------------------------------------
-- Trigger: force occurred_at on INSERT
-- ------------------------------------------------------------------
CREATE TRIGGER trg_event_force_occurred_at
BEFORE INSERT
ON audit.events
FOR EACH ROW
EXECUTE FUNCTION audit.tg_enforce_event_occurred_at();
