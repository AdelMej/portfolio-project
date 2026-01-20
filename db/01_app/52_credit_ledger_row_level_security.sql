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

    OR

    ------------------------------------------------------------------
    -- 3. System role
    ------------------------------------------------------------------
    pg_has_role(current_user, 'app_system', 'member')
);

COMMENT ON POLICY credit_ledger_select ON app.credit_ledger IS
'Users can see their own ledger entries, admins can see all, and system role has full visibility.';

-- ------------------------------------------------------------------
-- Policy: credit_ledger_insert_system
--
-- Only system role may INSERT ledger entries
-- ------------------------------------------------------------------
CREATE POLICY credit_ledger_insert_system
ON app.credit_ledger
FOR INSERT
WITH CHECK (
    pg_has_role(current_user, 'app_system', 'member')
);

COMMENT ON POLICY credit_ledger_insert_system ON app.credit_ledger IS
'Restricts insertion of ledger entries to system-level processes only.';

-- ------------------------------------------------------------------
-- Policy: credit_ledger_no_update
--
-- Prevents all updates to ledger entries (immutability)
-- ------------------------------------------------------------------
CREATE POLICY credit_ledger_no_update
ON app.credit_ledger
FOR UPDATE
USING (false)
WITH CHECK (false);

COMMENT ON POLICY credit_ledger_no_update ON app.credit_ledger IS
'Explicitly forbids updating any ledger entry; ledger entries are immutable once created.';
