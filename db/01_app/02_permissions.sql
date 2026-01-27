-- Revoke everything from PUBLIC (safety net)
REVOKE ALL ON DATABASE app FROM PUBLIC;
REVOKE ALL ON SCHEMA app FROM PUBLIC;

-- Allow app_user to connect
GRANT CONNECT ON DATABASE app TO app_user;

-- Allow app_user to see objects in schema
GRANT USAGE ON SCHEMA app TO app_user;

-- Explicitly forbid schema modification
REVOKE CREATE ON SCHEMA app FROM app_user;

-- Permissions on existing tables
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA app TO app_user;
REVOKE DELETE, TRUNCATE ON ALL TABLES IN SCHEMA app FROM app_user;

-- Permissions on existing sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_user;

-- Default privileges for future tables
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT, INSERT, UPDATE ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE DELETE, TRUNCATE ON TABLES FROM app_user;

-- Default privileges for future sequences
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- Extra comment for clarity
COMMENT ON ROLE app_user IS
'Application runtime role: no DDL, no DELETE/TRUNCATE, data access only';