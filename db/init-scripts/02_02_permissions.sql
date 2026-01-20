\c audit

-- ------------------------------------------------------------------
-- Permissions: audit database + schema
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Safety net: remove PUBLIC access
-- ------------------------------------------------------------------
REVOKE ALL ON DATABASE audit FROM PUBLIC;
REVOKE ALL ON SCHEMA audit FROM PUBLIC;

-- ------------------------------------------------------------------
-- app_system: controlled access
-- ------------------------------------------------------------------
-- Connect to audit database
GRANT CONNECT ON DATABASE audit TO app_system;

-- Visibility into schema
GRANT USAGE ON SCHEMA audit TO app_system;

-- Table access: only INSERT + SELECT
GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA audit TO app_system;

-- Forbid mutations
REVOKE UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_system;

-- Sequence access
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA audit TO app_system;

-- Default privileges for future tables/sequences
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT INSERT, SELECT ON TABLES TO app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
REVOKE UPDATE, DELETE, TRUNCATE ON TABLES FROM app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT USAGE, SELECT ON SEQUENCES TO app_system;

-- ------------------------------------------------------------------
-- app_admin: read-only
-- ------------------------------------------------------------------
-- Revoke mutation rights
REVOKE UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_admin;
REVOKE INSERT ON ALL TABLES IN SCHEMA audit FROM app_admin;

-- Default privileges for future tables
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM app_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT SELECT ON TABLES TO app_admin;

-- ------------------------------------------------------------------
-- Ownership restrictions
-- ------------------------------------------------------------------
REVOKE CREATE ON SCHEMA audit FROM app_admin;
ALTER SCHEMA audit OWNER TO postgres;

-- ------------------------------------------------------------------
-- Documentation
-- ------------------------------------------------------------------
COMMENT ON SCHEMA audit IS
'Append-only audit schema. No UPDATE/DELETE/TRUNCATE allowed, even for admin.';
