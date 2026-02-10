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
REVOKE ALL ON SCHEMA audit FROM PUBLIC;

-- ------------------------------------------------------------------
-- Connection permissions
--
-- Purpose:
-- - Allow only known application roles to connect
-- - Prevent anonymous or unintended access
-- ------------------------------------------------------------------

GRANT CONNECT ON DATABASE app TO app_user;
GRANT CONNECT ON DATABASE app TO app_system;
GRANT CONNECT ON DATABASE app TO app_admin;

-- ------------------------------------------------------------------
-- Schema ownership & visibility
--
-- Purpose:
-- - app_admin owns schemas and performs migrations
-- - Runtime roles may reference objects but never mutate schemas
-- ------------------------------------------------------------------

-- Ensure schema ownership
ALTER SCHEMA app OWNER TO app_admin;
ALTER SCHEMA audit OWNER TO app_admin;

-- Allow roles to resolve object names
GRANT USAGE ON SCHEMA app TO app_user;
GRANT USAGE ON SCHEMA app TO app_system;
GRANT USAGE ON SCHEMA audit TO app_system;
GRANT USAGE ON SCHEMA audit TO app_admin;

-- ------------------------------------------------------------------
-- Schema mutation lockdown
--
-- Purpose:
-- - Prevent application roles from creating or altering schema objects
-- - All DDL must go through app_admin
-- ------------------------------------------------------------------

REVOKE CREATE ON SCHEMA app FROM app_user;
REVOKE CREATE ON SCHEMA app FROM app_system;

REVOKE CREATE ON SCHEMA audit FROM app_user;
REVOKE CREATE ON SCHEMA audit FROM app_system;

-- ------------------------------------------------------------------
-- Table access: application schema (app)
--
-- Purpose:
-- - app_admin has full access (business rules enforced via constraints/RLS)
-- - app_user is read-only by default
-- - app_system has no implicit access
-- ------------------------------------------------------------------

-- Full access for schema owner
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA app
TO app_admin;

-- Read-only access for runtime API user
GRANT SELECT
ON ALL TABLES IN SCHEMA app
TO app_user;

-- ------------------------------------------------------------------
-- Table access: audit schema
--
-- Purpose:
-- - app_system may INSERT audit events only
-- - app_admin may SELECT audit data only
-- - Audit data is append-only and immutable
-- ------------------------------------------------------------------

-- Backend system may write audit events
GRANT INSERT
ON ALL TABLES IN SCHEMA audit
TO app_system;

-- Admins may observe audit data
GRANT SELECT
ON ALL TABLES IN SCHEMA audit
TO app_admin;

-- Explicitly forbid audit mutation (defense in depth)
REVOKE INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA audit
FROM app_admin;

-- ------------------------------------------------------------------
-- Sequence access
--
-- Purpose:
-- - app_admin controls sequences
-- - app_user can safely read sequence values
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
-- Function execution: application behavior (app_fcn)
--
-- Purpose:
-- - Centralize execution of application behavior
-- - Enforce strict separation between declarative access (RLS)
--   and imperative system operations (functions)
--
-- Execution model:
-- - app_user:
--     - Never executes functions directly
--     - Interacts with functions only indirectly via RLS predicates
--
-- - app_system:
--     - Executes application behavior explicitly
--     - Uses functions as transactional units of work
--     - No direct table access; all mutations go through functions
--
-- - app_admin:
--     - Owns and manages functions
--     - Used for migrations and maintenance only
--
-- Security rules:
-- - app_fcn schema is owned by app_admin
-- - SECURITY DEFINER functions explicitly control privilege escalation
-- - Non-SECURITY DEFINER functions execute with caller privileges
-- ------------------------------------------------------------------

-- Allow system role to resolve and execute application functions
GRANT USAGE ON SCHEMA app_fcn TO app_system;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA app_fcn TO app_system;

-- Prevent app_user from calling functions directly
REVOKE USAGE ON SCHEMA app_fcn FROM app_user;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA app_fcn FROM app_user;

-- Admin retains full control
GRANT USAGE ON SCHEMA app_fcn TO app_admin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA app_fcn TO app_admin;

-- ------------------------------------------------------------------
-- Default privileges (future-proofing)
--
-- Purpose:
-- - Ensure new objects inherit correct permissions automatically
-- - Prevent accidental privilege escalation in future migrations
-- ------------------------------------------------------------------

-- Revoke implicit defaults
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON TABLES FROM app_user, app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
REVOKE ALL ON SEQUENCES FROM app_system;

-- Admin always has full control over app schema data
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_admin;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO app_admin;

-- Runtime API users stay read-only by default
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT SELECT ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app
GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- Audit schema defaults
ALTER DEFAULT PRIVILEGES IN SCHEMA audit
GRANT INSERT ON TABLES TO app_system;

ALTER DEFAULT PRIVILEGES IN SCHEMA audit
GRANT SELECT ON TABLES TO app_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA audit
REVOKE INSERT, UPDATE, DELETE ON TABLES FROM app_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA audit
REVOKE ALL ON TABLES FROM PUBLIC;

-- app_fcn defaults
ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app_fcn
GRANT EXECUTE ON FUNCTIONS TO app_system;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app_fcn
REVOKE ALL ON FUNCTIONS FROM app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE app_admin IN SCHEMA app_fcn
GRANT EXECUTE ON FUNCTIONS TO app_admin;

-- ------------------------------------------------------------------
-- Role documentation
--
-- Purpose:
-- - Make intent explicit for future maintainers
-- - Acts as living documentation inside the database
-- ------------------------------------------------------------------

COMMENT ON ROLE app_admin IS
'Schema owner and migration role. Full access to application data. Audit data is read-only. All invariants enforced via constraints, triggers, and RLS.';

COMMENT ON ROLE app_user IS
'Application runtime role. No DDL, no DELETE/TRUNCATE. Least-privilege: SELECT by default, writes only via explicit grants and RLS.';

COMMENT ON ROLE app_system IS
'Backend system role. Write-only access where explicitly granted (e.g. audit events). No read access unless explicitly allowed.';
