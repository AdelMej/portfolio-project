\c app

-- Enable and enforce RLS
ALTER TABLE app.coach_stripe_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.coach_stripe_accounts FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- RLS: app.coach_stripe_accounts
--
-- Purpose:
-- - Allow coaches to view their own Stripe Connect account state
--
-- Access model:
-- - app_user (coach):
--   - SELECT only
--   - Restricted to self via RLS
--
-- Ownership model:
-- - Stripe lifecycle and mutations are system-owned
-- - No direct user writes (enforced via privileges + RLS)
--
-- Guarantees:
-- - Only users with the coach role may see records
-- - Coaches can only see their own Stripe account linkage
-- - All mutations occur via SECURITY DEFINER functions
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Policy: coach_stripe_account_select
-- ------------------------------------------------------------------
CREATE POLICY coach_stripe_account_select
ON app.coach_stripe_accounts
FOR SELECT
TO app_user
USING (
    app_fcn.is_coach()
    AND app_fcn.is_self(coach_id)
);

COMMENT ON POLICY coach_stripe_account_select ON app.coach_stripe_accounts IS
'Allows coaches (app_user) to read their own Stripe account linkage. 
Stripe lifecycle and mutations are system-owned and performed exclusively via SECURITY DEFINER functions.';