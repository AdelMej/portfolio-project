-- ------------------------------------------------------------------
-- Global privilege hardening
--
-- Purpose:
-- - Remove implicit access granted via PUBLIC
-- - Enforce explicit, least-privilege access model
--
-- Notes:
-- - PUBLIC privileges are a common source of privilege leaks
-- - All access must be explicitly granted per role
-- ------------------------------------------------------------------

-- Revoke everything from PUBLIC (safety net)
REVOKE ALL ON DATABASE app FROM PUBLIC;
REVOKE ALL ON SCHEMA app FROM PUBLIC;

-- ------------------------------------------------------------------
-- Connection permissions
--
-- Purpose:
-- - Allow only application roles to connect
-- - Prevent anonymous or unintended access
-- ------------------------------------------------------------------

-- Allow application runtime user to connect
GRANT CONNECT ON DATABASE app TO app_user;

-- Allow application system role to connect
GRANT CONNECT ON DATABASE app TO app_system;

-- ------------------------------------------------------------------
-- Schema visibility
--
-- Purpose:
-- - Allow roles to reference objects in app schema
-- - USAGE does NOT allow object creation or modification
-- ------------------------------------------------------------------

-- Allow app_user to see objects in schema
GRANT USAGE ON SCHEMA app TO app_user;

-- Allow app_system to see objects in schema
GRANT USAGE ON SCHEMA app TO app_system;

-- ------------------------------------------------------------------
-- Schema mutation lockdown
--
-- Purpose:
-- - Prevent application roles from creating or altering schema objects
-- - All DDL must go through app_admin
-- ------------------------------------------------------------------

-- Explicitly forbid schema modification
REVOKE CREATE ON SCHEMA app FROM app_user;
REVOKE CREATE ON SCHEMA app FROM app_system;

-- ------------------------------------------------------------------
-- Table access
--
-- Purpose:
-- - app_user is read-only by default
-- - Writes are granted explicitly per table and controlled via RLS
-- ------------------------------------------------------------------

-- Tables
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_user;

-- ------------------------------------------------------------------
-- Sequence access
--
-- Purpose:
-- - Allow reading sequence values (e.g. currval)
-- - Prevent unauthorized sequence manipulation
-- ------------------------------------------------------------------

-- Sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_user;

-- ------------------------------------------------------------------
-- Default privileges (future-proofing)
--
-- Purpose:
-- - Ensure new objects inherit correct permissions automatically
-- - Prevent accidental privilege escalation on future migrations
-- ------------------------------------------------------------------

-- Revoke all default table privileges for app roles
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON TABLES FROM app_user, app_system;

-- Revoke all default sequence privileges for app_system
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON SEQUENCES FROM app_system;

-- Grant default read-only access to app_user
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- ------------------------------------------------------------------
-- Role documentation
--
-- Purpose:
-- - Make intent explicit for future maintainers
-- - Acts as living documentation inside the database
-- ------------------------------------------------------------------

COMMENT ON ROLE app_user IS
'Application runtime role. No DDL, no DELETE/TRUNCATE. Least-privilege: SELECT by default, writes only via explicit grants and RLS.';