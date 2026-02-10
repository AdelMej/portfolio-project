\c app

-- ------------------------------------------------------------------
-- Triggers: app.payment
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: enforce immutability
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_payment_immutable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'payment table is immutable; rows cannot be updated or deleted';
END;
$$;

COMMENT ON FUNCTION app.tg_payment_immutable() IS
'Prevents any UPDATE or DELETE on the payment table to guarantee immutable payment records.';

-- ------------------------------------------------------------------
-- Trigger: prevent updates
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_no_update
BEFORE UPDATE ON app.payments
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_immutable();

COMMENT ON TRIGGER trg_payment_no_update ON app.payments IS
'Prevents modification of any payment row; all payments are immutable.';

-- ------------------------------------------------------------------
-- Trigger: prevent deletes
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_no_delete
BEFORE DELETE ON app.payments
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_immutable();

COMMENT ON TRIGGER trg_payment_no_delete ON app.payments IS
'Prevents deletion of any payment row; all payments are append-only.';

-- ------------------------------------------------------------------
-- Function: enforce idempotency (optional)
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_payment_idempotency_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM app.payments p
        WHERE p.provider = NEW.provider
          AND p.provider_payment_id = NEW.provider_payment_id
    ) THEN
        RAISE EXCEPTION 'Duplicate provider payment detected: % / %',
            NEW.provider, NEW.provider_payment_id;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_payment_idempotency_guard() IS
'Prevents insertion of duplicate payments based on provider + provider_payment_id.';

-- ------------------------------------------------------------------
-- Trigger: enforce idempotency
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_idempotency_guard
BEFORE INSERT ON app.payments
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_idempotency_guard();

COMMENT ON TRIGGER trg_payment_idempotency_guard ON app.payments IS
'Ensures each payment inserted is unique by provider and provider_payment_id to enforce idempotency.';
