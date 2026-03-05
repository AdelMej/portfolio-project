-- ------------------------------------------------------------------
-- Row Level Security: app.credit_ledger
--
-- Visibility model:
-- - Users see only their own ledger entries
-- - Admins see all ledger entries
-- - System role has full visibility
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.credit_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.credit_ledger FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: credit_ledger_select
--
-- Controls who can SELECT ledger entries
-- ------------------------------------------------------------------
CREATE POLICY credit_ledger_select
ON app.credit_ledger
FOR SELECT
USING (
    app_fcn.is_self(user_id)
    OR app_fcn.is_admin()
);

COMMENT ON POLICY credit_ledger_select ON app.credit_ledger IS
'Users can see their own ledger entries, admins can see all, and system role has full visibility.';
