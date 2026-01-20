-- ------------------------------------------------------------------
-- Database: audit
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Purpose:
-- - Separate database for auditing activities
-- - Owned and controlled by the database administrator (app_admin)
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Create audit database
-- ------------------------------------------------------------------
CREATE DATABASE audit
OWNER app_admin;

COMMENT ON DATABASE audit IS
'Dedicated database for storing audit logs and monitoring data; owned by app_admin.';

-- ------------------------------------------------------------------
-- Switch to audit database
-- ------------------------------------------------------------------
\c audit

-- ------------------------------------------------------------------
-- Schema: audit
-- ------------------------------------------------------------------
CREATE SCHEMA audit
AUTHORIZATION app_admin;

COMMENT ON SCHEMA audit IS
'Schema within audit database to contain all auditing tables, views, and functions; owned by app_admin.';
