-- ------------------------------------------------------------------
-- Triggers: app.credit_ledger
-- ------------------------------------------------------------------
-- Purpose:
-- - Enforce append-only ledger semantics
-- - Guarantee balance consistency
-- - Maintain cause ↔ payment_intent correctness
-- - Enforce temporal order of ledger entries
--
-- Guarantees:
-- - Ledger entries cannot be updated or deleted
-- - balance_after_cents is always previous_balance + amount_cents
-- - payment_intent_id is correctly set according to cause
-- - Ledger entries are strictly chronological
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: enforce immutability (no updates or deletes)
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_credit_ledger_immutable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'credit_ledger is append-only';
END;
$$;

COMMENT ON FUNCTION app.tg_credit_ledger_immutable() IS
'Prevents any UPDATE or DELETE on credit_ledger to maintain an immutable audit trail.';

-- Trigger: prevent updates
CREATE TRIGGER trg_credit_ledger_no_update
BEFORE UPDATE ON app.credit_ledger
FOR EACH ROW
EXECUTE FUNCTION app.tg_credit_ledger_immutable();

COMMENT ON TRIGGER trg_credit_ledger_no_update ON app.credit_ledger IS
'Prevents modification of existing ledger entries.';

-- Trigger: prevent deletes
CREATE TRIGGER trg_credit_ledger_no_delete
BEFORE DELETE ON app.credit_ledger
FOR EACH ROW
EXECUTE FUNCTION app.tg_credit_ledger_immutable();

COMMENT ON TRIGGER trg_credit_ledger_no_delete ON app.credit_ledger IS
'Prevents deletion of any ledger entry.';

-- ------------------------------------------------------------------
-- Function: balance consistency guard
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_credit_ledger_balance_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_last_balance INTEGER;
BEGIN
    -- Fetch the most recent balance for the user
    SELECT balance_after_cents
    INTO v_last_balance
    FROM app.credit_ledger
    WHERE user_id = NEW.user_id
    ORDER BY created_at DESC
    LIMIT 1;

    IF v_last_balance IS NULL THEN
        v_last_balance := 0;
    END IF;

    IF NEW.balance_after_cents <> v_last_balance + NEW.amount_cents THEN
        RAISE EXCEPTION
            'Invalid ledger balance: expected %, got %',
            v_last_balance + NEW.amount_cents,
            NEW.balance_after_cents;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_credit_ledger_balance_guard() IS
'Ensures balance_after_cents is consistent with previous balance plus amount_cents.';

-- Trigger: validate balance on insert
CREATE TRIGGER trg_credit_ledger_balance_guard
BEFORE INSERT ON app.credit_ledger
FOR EACH ROW
EXECUTE FUNCTION app.tg_credit_ledger_balance_guard();

COMMENT ON TRIGGER trg_credit_ledger_balance_guard ON app.credit_ledger IS
'Validates balance continuity for each new ledger entry.';

-- ------------------------------------------------------------------
-- Function: enforce cause ↔ payment_intent correctness
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_credit_ledger_cause_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.cause IN ('payment', 'refund') AND NEW.payment_intent_id IS NULL THEN
        RAISE EXCEPTION 'payment_intent_id required for %', NEW.cause;
    END IF;

    IF NEW.cause NOT IN ('payment', 'refund') AND NEW.payment_intent_id IS NOT NULL THEN
        RAISE EXCEPTION 'payment_intent_id forbidden for %', NEW.cause;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_credit_ledger_cause_guard() IS
'Ensures payment_intent_id is set correctly according to ledger cause.';

-- Trigger: enforce cause rules
CREATE TRIGGER trg_credit_ledger_cause_guard
BEFORE INSERT ON app.credit_ledger
FOR EACH ROW
EXECUTE FUNCTION app.tg_credit_ledger_cause_guard();

COMMENT ON TRIGGER trg_credit_ledger_cause_guard ON app.credit_ledger IS
'Prevents semantic corruption of ledger entries by validating cause ↔ payment_intent relationship.';

-- ------------------------------------------------------------------
-- Function: enforce temporal consistency
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_credit_ledger_time_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_last_ts TIMESTAMPTZ;
BEGIN
    SELECT created_at
    INTO v_last_ts
    FROM app.credit_ledger
    WHERE user_id = NEW.user_id
    ORDER BY created_at DESC
    LIMIT 1;

    IF v_last_ts IS NOT NULL AND NEW.created_at < v_last_ts THEN
        RAISE EXCEPTION 'Ledger entries must be chronological';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_credit_ledger_time_guard() IS
'Prevents inserting backdated ledger entries, ensuring strict chronological order per user.';

-- Trigger: enforce temporal order
CREATE TRIGGER trg_credit_ledger_time_guard
BEFORE INSERT ON app.credit_ledger
FOR EACH ROW
EXECUTE FUNCTION app.tg_credit_ledger_time_guard();

COMMENT ON TRIGGER trg_credit_ledger_time_guard ON app.credit_ledger IS
'Guarantees that ledger entries are inserted in chronological order for each user.';
