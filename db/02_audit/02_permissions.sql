\c audit

-- ------------------------------------------------------------------
-- Permissions: audit database + schema
--
-- Model:
-- - audit is append-only
-- - app_system can INSERT + SELECT
-- - app_admin is STRICTLY read-only
-- - no role may UPDATE / DELETE / TRUNCATE
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Safety net: remove PUBLIC access
-- ------------------------------------------------------------------
REVOKE ALL ON DATABASE audit FROM PUBLIC;
REVOKE ALL ON SCHEMA audit FROM PUBLIC;

-- ------------------------------------------------------------------
-- app_system: controlled access (writer + reader)
-- ------------------------------------------------------------------

-- Allow connection
GRANT CONNECT ON DATABASE audit TO app_system;

-- Allow schema visibility
GRANT USAGE ON SCHEMA audit TO app_system;

-- Allow append + read
GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA audit TO app_system;

-- Explicitly forbid mutation
REVOKE UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_system;

-- Sequence access (for SERIAL / IDENTITY)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA audit TO app_system;

-- Default privileges for future objects
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
    GRANT INSERT, SELECT ON TABLES TO app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
    REVOKE UPDATE, DELETE, TRUNCATE ON TABLES FROM app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
    GRANT USAGE, SELECT ON SEQUENCES TO app_system;

-- ------------------------------------------------------------------
-- app_admin: read-only auditor
-- ------------------------------------------------------------------

-- Allow connection
GRANT CONNECT ON DATABASE audit TO app_admin;

-- Allow schema visibility
GRANT USAGE ON SCHEMA audit TO app_admin;

-- Allow read-only access on existing tables
GRANT SELECT ON ALL TABLES IN SCHEMA audit TO app_admin;

-- Explicitly forbid all writes
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_admin;

-- Default privileges for future tables
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
    GRANT SELECT ON TABLES TO app_admin;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
    REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM app_admin;

-- ------------------------------------------------------------------
-- Ownership restrictions
-- ------------------------------------------------------------------

-- Prevent schema modifications
REVOKE CREATE ON SCHEMA audit FROM app_admin;

-- Ensure ownership is NOT app_admin
ALTER SCHEMA audit OWNER TO postgres;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------
COMMENT ON SCHEMA audit IS
'Append-only audit schema. app_system may INSERT + SELECT. app_admin is read-only. UPDATE/DELETE/TRUNCATE are forbidden for all non-superusers.';
