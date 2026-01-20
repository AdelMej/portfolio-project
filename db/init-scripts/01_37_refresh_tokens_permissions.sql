\c app

-- ------------------------------------------------------------------
-- Privileges: app.refresh_tokens
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user
--
-- - No direct access
-- - All operations blocked via RLS
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE app.refresh_tokens FROM app_user;

-- ------------------------------------------------------------------
-- app_admin
--
-- - Read-only access to all tokens
-- - Used for auditing / inspections
-- ------------------------------------------------------------------
GRANT SELECT ON TABLE app.refresh_tokens TO app_admin;

-- ------------------------------------------------------------------
-- app_system
--
-- - Full lifecycle control (except DELETE, RLS prevents deletion)
-- - Used for issuing, revoking, and updating refresh tokens
-- ------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE ON TABLE app.refresh_tokens TO app_system;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE app.refresh_tokens IS
'Refresh token management table.
RLS policies enforce:
- Users see only their own tokens
- Admins see all tokens
- System role may insert and update tokens
Privileges:
- app_user: no access
- app_admin: read-only
- app_system: full lifecycle control (except deletion)';
