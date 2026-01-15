-- Safety net: remove PUBLIC access
REVOKE ALL ON DATABASE audit FROM PUBLIC;
REVOKE ALL ON SCHEMA audit FROM PUBLIC;

-- Allow app_system to connect
GRANT CONNECT ON DATABASE audit TO app_system;

-- Allow visibility into schema
GRANT USAGE ON SCHEMA audit TO app_system;

-- Allow INSERT + SELECT only on existing tables
GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA audit TO app_system;

-- Absolutely forbid mutations
REVOKE UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_system;

-- Sequences (if any)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA audit TO app_system;

-- DEFAULT PRIVILEGES (future-proof)
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT INSERT, SELECT ON TABLES TO app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
REVOKE UPDATE, DELETE, TRUNCATE ON TABLES FROM app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT USAGE, SELECT ON SEQUENCES TO app_system;

-- Admin can read but cannot mutate audit data
REVOKE UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA audit FROM app_admin;

-- Optional but recommended: forbid admin inserts too
REVOKE INSERT ON ALL TABLES IN SCHEMA audit FROM app_admin;

-- DEFAULT PRIVILEGES (future-proof)
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM app_admin;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA audit
GRANT SELECT ON TABLES TO app_admin;

-- big BONK
REVOKE CREATE ON SCHEMA audit FROM app_admin;
ALTER SCHEMA audit OWNER TO postgres;

-- Documentation
COMMENT ON SCHEMA audit IS
'Append-only audit schema. No UPDATE/DELETE/TRUNCATE allowed, even for admin.';