\c app

-- ------------------------------------------------------------------
-- Permissions: app.invite_tokens
--
-- Overview:
-- - Stores invitation tokens used for onboarding flows
-- - Tokens are created, consumed, and revoked exclusively via backend logic
-- - No application role interacts with this table directly
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Regular authenticated application users
--
-- Capabilities (GRANTs):
-- - None
--
-- Scope (RLS):
-- - No direct access to invite tokens
-- - Users may only observe invite-related state through controlled endpoints
-- ---------------------------------------------------------------

REVOKE ALL
ON TABLE app.invite_tokens
FROM app_user;

-- Note:
-- All invite token lifecycle operations are performed via backend-owned
-- SECURITY DEFINER functions. No direct table privileges are granted to
-- application roles.

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.invite_tokens IS
'Invitation token table used for onboarding workflows.
No application role has direct table privileges.
All access and lifecycle management is handled via backend logic and
SECURITY DEFINER functions.';