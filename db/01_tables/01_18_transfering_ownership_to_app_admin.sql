-- ------------------------------------------------------------------
-- Schema ownership normalization
--
-- Purpose:
-- - Ensure app_admin is the owner of ALL application tables
-- - Fix permission issues caused by tables created by other roles
-- - Make GRANTs, RLS, and default privileges actually effective
--
-- Why this exists (important):
-- - In PostgreSQL, GRANTs do NOT override ownership rules
-- - If app_admin does not own a table:
--     - permission denied errors occur even with correct GRANTs
--     - ALTER DEFAULT PRIVILEGES may not apply as expected
--     - RLS debugging becomes extremely confusing
--
-- When to run:
-- - After initial schema creation
-- - After importing dumps created by another role
-- - If "permission denied" appears despite correct GRANTs
--
-- Notes:
-- - This is intentionally explicit (no loops / automation)
-- - Ownership transfer is a one-time normalization step
-- - Safe to re-run (idempotent with same owner)
-- ------------------------------------------------------------------
ALTER TABLE app.users OWNER TO app_admin;
ALTER TABLE app.user_profiles OWNER TO app_admin;
ALTER TABLE app.roles OWNER TO app_admin;
ALTER TABLE app.roles OWNER TO app_admin;
ALTER TABLE app.user_roles OWNER TO app_admin;
ALTER TABLE app.sessions OWNER TO app_admin;
ALTER TABLE app.payment_intents OWNER TO app_admin;
ALTER TABLE app.refresh_tokens OWNER TO app_admin;
ALTER TABLE app.invite_tokens OWNER TO app_admin;
ALTER TABLE app.session_participation OWNER TO app_admin;
ALTER TABLE app.session_attendance OWNER TO app_admin;
ALTER TABLE app.credit_ledger OWNER TO app_admin;
ALTER TABLE app.payment OWNER TO app_admin;*
ALTER TABLE app.coach_stripe_accounts OWNER TO app_admin;
ALTER TABLE audit.event OWNER TO app_admin;