-- ------------------------------------------------------------------
-- Permissions: app.refresh_tokens
--
-- Overview:
-- - Stores refresh tokens for authentication
-- - Table is intentionally locked down at the GRANT level
-- - All access is mediated through RLS and SECURITY DEFINER functions
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
-- - No direct table access
-- - Any interaction is performed indirectly via functions
-- ---------------------------------------------------------------

REVOKE ALL ON TABLE app.refresh_tokens FROM app_user;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.refresh_tokens IS
'Refresh token storage table.
No application role has direct table privileges.
All access is enforced via RLS and SECURITY DEFINER functions.
Used for secure token issuance, rotation, and validation.';
