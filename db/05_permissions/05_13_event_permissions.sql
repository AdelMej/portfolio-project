-- ------------------------------------------------------------------
-- Privileges: audit.events
--
-- Purpose:
-- - Store system and domain events (audit / observability)
--
-- Design notes:
-- - Append-only table
-- - No direct INSERT / UPDATE / DELETE privileges
-- - All writes are performed via SECURITY DEFINER functions
-- - app_system has no direct table access
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Privilege cleanup
-- ------------------------------------------------------------------
REVOKE ALL ON TABLE audit.events FROM app_user;
REVOKE ALL ON TABLE audit.events FROM app_admin;
REVOKE ALL ON TABLE audit.events FROM app_system;

-- ------------------------------------------------------------------
-- app_admin: read-only
--
-- Notes:
-- - Used for auditing, debugging, and support
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE audit.events
TO app_admin;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------

COMMENT ON TABLE audit.events IS
'System and domain event log.
Append-only table written exclusively via SECURITY DEFINER functions.
Only app_admin may read events; no role has direct write privileges.';
