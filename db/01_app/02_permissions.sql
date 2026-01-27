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

-- Allow schema / migration admin to connect
GRANT CONNECT ON DATABASE app TO app_admin;

-- ------------------------------------------------------------------
-- Schema ownership & visibility
--
-- Purpose:
-- - app_admin owns the schema and all objects
-- - Runtime roles may reference objects but not mutate schema
-- ------------------------------------------------------------------

-- Ensure schema ownership
ALTER SCHEMA app OWNER TO app_admin;

-- Allow roles to see objects in schema
GRANT USAGE ON SCHEMA app TO app_user;
GRANT USAGE ON SCHEMA app TO app_system;

-- ------------------------------------------------------------------
-- Schema mutation lockdown
--
-- Purpose:
-- - Prevent application roles from creating or altering schema objects
-- - All DDL must go through app_admin
-- ------------------------------------------------------------------

REVOKE CREATE ON SCHEMA app FROM app_user;
REVOKE CREATE ON SCHEMA app FROM app_system;

-- ------------------------------------------------------------------
-- Table access
--
-- Purpose:
-- - app_admin has full data access (business rules enforced elsewhere)
-- - app_user is read-only by default
-- - app_system gets no implicit access
-- ------------------------------------------------------------------

-- Full access for schema owner
GRANT SELECT, INSERT, UPDATE
ON ALL TABLES IN SCHEMA app
TO app_admin;

-- Read-only access for runtime users
GRANT SELECT
ON ALL TABLES IN SCHEMA app
TO app_user;

-- ------------------------------------------------------------------
-- Sequence access
--
-- Purpose:
-- - app_admin controls sequences
-- - app_user can read sequence values safely
-- ------------------------------------------------------------------

-- Full sequence control for admin
GRANT USAGE, SELECT, UPDATE
ON ALL SEQUENCES IN SCHEMA app
TO app_admin;

-- Read-only sequence access for app_user
GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA app
TO app_user;

-- ------------------------------------------------------------------
-- Default privileges (future-proofing)
--
-- Purpose:
-- - Ensure new objects inherit correct permissions automatically
-- - Prevent accidental privilege escalation in future migrations
-- ------------------------------------------------------------------

-- Revoke all defaults for runtime roles
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON TABLES FROM app_user, app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON SEQUENCES FROM app_system;

-- Ensure admin always has full control
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_admin;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO app_admin;

-- Ensure runtime users stay read-only by default
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

COMMENT ON ROLE app_admin IS
'Schema owner and migration role. Full data access. No business rules enforced via privileges; constraints, triggers, and RLS apply.';

COMMENT ON ROLE app_user IS
'Application runtime role. No DDL, no DELETE/TRUNCATE. Least-privilege: SELECT by default, writes only via explicit grants and RLS.';

COMMENT ON ROLE app_system IS
'Backend system role. Writes allowed only where explicitly granted and governed by RLS.';
