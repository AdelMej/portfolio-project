-- ------------------------------------------------------------------
-- Row Level Security: app.payment
--
-- Visibility model:
-- - Users can see their own payments
-- - Admins can see all payments
-- - System can insert new payments
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.payments FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: payment_select
--
-- Controls who can SELECT payment records
-- ------------------------------------------------------------------
CREATE POLICY payment_select
ON app.payments
FOR SELECT
USING (
    app_fcn.is_self(user_id)

    OR app_fcn.is_admin()
);

COMMENT ON POLICY payment_select ON app.payments IS
'Allows users to see their own payments and admins to see all payments.';