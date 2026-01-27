-- ------------------------------------------------------------------
-- Row Level Security: app.payment
--
-- Visibility model:
-- - Users can see their own payments
-- - Admins can see all payments
-- - System can insert new payments
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.payment ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.payment FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: payment_select
--
-- Controls who can SELECT payment records
-- ------------------------------------------------------------------
CREATE POLICY payment_select
ON app.payment
FOR SELECT
USING (
    ------------------------------------------------------------------
    -- 1. Self
    ------------------------------------------------------------------
    user_id = current_setting('app.current_user_id')::uuid

    OR

    ------------------------------------------------------------------
    -- 2. App-level admin
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY payment_select ON app.payment IS
'Allows users to see their own payments and admins to see all payments.';

-- ------------------------------------------------------------------
-- Policy: payment_insert_system
--
-- Only system role can insert payments
-- ------------------------------------------------------------------
CREATE POLICY payment_insert_system
ON app.payment
FOR INSERT
WITH CHECK (
    pg_has_role(current_user, 'app_system', 'member')
);

COMMENT ON POLICY payment_insert_system ON app.payment IS
'Allows only the system (app_system) to insert new payments.';

-- ------------------------------------------------------------------
-- Policy: payment_update_prevent
--
-- No one can update a payment (immutable after insertion)
-- ------------------------------------------------------------------
CREATE POLICY payment_update_prevent
ON app.payment
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

COMMENT ON POLICY payment_update_prevent ON app.payment IS
'Prevents any updates to payment records; payments are immutable after creation.';
