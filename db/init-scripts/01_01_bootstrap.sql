-- ------------------------------------------------------------------
-- Database: app
--
-- Purpose:
-- - Primary application database
-- - Hosts all application-owned schemas, tables, roles, and logic
--
-- Ownership model:
-- - Owned by app_admin (database owner)
-- - app_admin is responsible for:
--   - migrations
--   - schema changes
--   - role management
--   - emergency access
--
-- Notes:
-- - No application runtime role should own the database
-- - Ownership is intentionally centralized
-- ------------------------------------------------------------------

-- Create the application database
CREATE DATABASE app
    OWNER app_admin;

-- ------------------------------------------------------------------
-- Switch connection to the application database
-- Required before creating schemas or objects inside it
-- ------------------------------------------------------------------
\c app

-- ------------------------------------------------------------------
-- Schema: app
--
-- Purpose:
-- - Logical namespace for all application objects
-- - Contains:
--   - tables
--   - types
--   - functions
--   - triggers
--   - RLS policies
--
-- Ownership model:
-- - Owned by app_admin
-- - Prevents privilege confusion
-- - Allows strict GRANT-based access control
--
-- Notes:
-- - No objects should be created in public schema
-- - All application objects live under app.*
-- ------------------------------------------------------------------

-- Create application schema owned by admin
CREATE SCHEMA app
    AUTHORIZATION app_admin;