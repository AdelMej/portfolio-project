\c app

-- ------------------------------------------------------------------
-- Privileges: app.invite_tokens
--
-- Purpose:
-- - Manage invitation links for onboarding users
-- - Tokens are generated and consumed exclusively by backend logic
-- - Users may only observe invite status through controlled endpoints
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: no direct access
--
-- Notes:
-- - Regular users never create, revoke, or read invite tokens directly
-- - All invite flows are mediated by the backend (app_system)
-- ------------------------------------------------------------------
REVOKE ALL
ON TABLE app.invite_tokens
FROM app_user;

COMMENT ON TABLE app.invite_tokens IS
'Invitation tokens used for onboarding flows. Regular users (app_user) have no direct access; all invite operations are performed by backend logic and constrained by RLS.';

-- ------------------------------------------------------------------
-- app_system: invitation authority
--
-- Used by:
-- - Invite link generation
-- - Invite validation & consumption
-- - Expiry and cleanup jobs
--
-- Guarantees:
-- - Full CRUD access for backend workflows
-- - RLS still applies to prevent cross-tenant or invalid access
-- ------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE app.invite_tokens
TO app_system;

COMMENT ON TABLE app.invite_tokens IS
'Backend system role (app_system) manages invitation tokens. Full CRUD access is granted for invite generation and consumption, with row-level security enforcing scope and ownership.';

-- ------------------------------------------------------------------
-- app_admin: database administrator
--
-- Notes:
-- - Full visibility for debugging and recovery
-- - Bypasses RLS via role attribute
-- ------------------------------------------------------------------
GRANT ALL
ON TABLE app.invite_tokens
TO app_admin;

COMMENT ON TABLE app.invite_tokens IS
'Administrative access to invitation tokens. app_admin has unrestricted privileges and bypasses RLS for maintenance and emergency operations.';