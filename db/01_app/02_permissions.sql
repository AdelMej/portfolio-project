-- Revoke everything from PUBLIC (safety net)
REVOKE ALL ON DATABASE app FROM PUBLIC;
REVOKE ALL ON SCHEMA app FROM PUBLIC;

-- Allow app_user to connect
GRANT CONNECT ON DATABASE app TO app_user;

-- Allow app_user to see objects in schema
GRANT USAGE ON SCHEMA app TO app_user;

-- Allow app_system to connect
GRANT CONNECT ON DATABASE app TO app_system;

-- Allow app_system  to see objects in schema
GRANT USAGE ON SCHEMA app TO app_system;

-- Explicitly forbid schema modification
REVOKE CREATE ON SCHEMA app FROM app_user;
REVOKE CREATE ON SCHEMA app FROM app_system;

-- Tables
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_user;

-- Sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_user;

-- default permission
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON TABLES FROM app_user, app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON SEQUENCES FROM app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT ON SEQUENCES TO app_user;


-- Extra comment for clarity
COMMENT ON ROLE app_user IS
'Application runtime role. No DDL, no DELETE/TRUNCATE. Least-privilege: SELECT by default, writes only via explicit grants + RLS.';