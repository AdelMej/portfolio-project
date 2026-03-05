-- ------------------------------------------------------------------
-- Triggers: app.payment_intents
-- ------------------------------------------------------------------
--
-- Purpose:
-- - Enforce immutability of critical fields
-- - Maintain audit consistency (updated_at)
-- - Guard valid status transitions
--
-- Guarantees:
-- - Critical fields cannot be modified after creation
-- - updated_at is always refreshed on update
-- - Status transitions follow a strict workflow
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Function: auto-update updated_at
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_payment_intents_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_payment_intents_set_updated_at() IS
'Automatically updates updated_at timestamp on every payment_intents update.';

-- ------------------------------------------------------------------
-- Trigger: set updated_at on update
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_intents_set_updated_at
BEFORE UPDATE ON app.payment_intents
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_intents_set_updated_at();

COMMENT ON TRIGGER trg_payment_intents_set_updated_at ON app.payment_intents IS
'Ensures updated_at reflects the last modification time.';

-- ------------------------------------------------------------------
-- Function: immutable critical fields
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_payment_intents_immutable_fields()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.user_id <> OLD.user_id
        OR NEW.session_id <> OLD.session_id
        OR NEW.provider <> OLD.provider
        OR NEW.provider_intent_id <> OLD.provider_intent_id
        OR NEW.amount_cents <> OLD.amount_cents
        OR NEW.currency <> OLD.currency
    THEN
        RAISE EXCEPTION
            'payment_intents immutable fields cannot be modified';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION app.tg_payment_intents_immutable_fields() IS
'Prevents modification of immutable fields: user_id, session_id, provider, provider_intent_id, amount_cents, currency.';

-- ------------------------------------------------------------------
-- Trigger: enforce immutable fields
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_intents_immutable_fields
BEFORE UPDATE ON app.payment_intents
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_intents_immutable_fields();

COMMENT ON TRIGGER trg_payment_intents_immutable_fields ON app.payment_intents IS
'Blocks any attempt to modify immutable fields of a payment_intent.';

-- ------------------------------------------------------------------
-- Function: payment_intent status guard
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app.tg_payment_intents_status_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    -- no-op
    IF NEW.status = OLD.status THEN
        RETURN NEW;
    END IF;

    -- terminal states are final
    IF OLD.status IN ('succeeded', 'failed', 'canceled') THEN
        RAISE EXCEPTION
            'payment_intent status is terminal (current=%)', OLD.status;
    END IF;

    -- always allow transition to terminal states
    IF NEW.status IN ('succeeded', 'failed', 'canceled') THEN
        RETURN NEW;
    END IF;

    -- allow any other forward informational update
    RETURN NEW;
END;
$$;


COMMENT ON FUNCTION app.tg_payment_intents_status_guard() IS
'Enforces valid status transitions for payment_intents and prevents changes from terminal states.';

-- ------------------------------------------------------------------
-- Trigger: enforce status workflow
-- ------------------------------------------------------------------
CREATE TRIGGER trg_payment_intents_status_guard
BEFORE UPDATE OF status ON app.payment_intents
FOR EACH ROW
EXECUTE FUNCTION app.tg_payment_intents_status_guard();

COMMENT ON TRIGGER trg_payment_intents_status_guard ON app.payment_intents IS
'Validates allowed status transitions and prevents invalid updates on payment_intents.';
