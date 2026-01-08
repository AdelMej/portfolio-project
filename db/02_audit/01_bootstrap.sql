-- Create the audit database
CREATE DATABASE audit OWNER app_admin;

-- Switch to audit database
\c audit

-- Create audit schema owned by admin
CREATE SCHEMA audit AUTHORIZATION app_admin;