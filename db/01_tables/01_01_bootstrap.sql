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

-- ------------------------------------------------------------------
-- Schema: audit
--
-- Purpose:
-- - Logical namespace for all audit-related objects
-- - Contains:
--   - append-only audit tables (e.g. events)
--   - audit-specific functions and triggers
--
-- Design principles:
-- - Append-only (no UPDATE / DELETE)
-- - Written in the same transaction as business data
-- - Used for compliance, debugging, and observability
-- - Never used to drive business logic or invariants
--
-- Ownership model:
-- - Owned by app_admin
-- - Application role has INSERT-only access
-- - Read access granted selectively (e.g. admin, analytics)
--
-- Notes:
-- - Audit data represents observed facts, not state
-- - Mutations are forbidden at the database level
-- - Separation via schema (not separate DB) guarantees atomicity
-- ------------------------------------------------------------------

-- Create audit schema owned by admin
CREATE SCHEMA audit
    AUTHORIZATION app_admin;

-- ------------------------------------------------------------------
-- Schema: app_fcn
--
-- Purpose:
-- - Logical namespace for all application-level database functions
-- - Centralizes domain logic executed inside the database
--
-- Contains:
-- - Domain predicate functions (e.g. is_admin, can_read_user)
-- - System work functions (unit-of-work / transactional jobs)
-- - Helper functions shared across RLS, triggers, and system logic
--
-- Design principles:
-- - Functions define and enforce business invariants
-- - Database is the source of truth for correctness
-- - Functions may raise explicit domain errors
-- - Fail-fast is preferred over silent behavior
--
-- Security model:
-- - Schema owned by app_admin
-- - Functions may be:
--     - SECURITY DEFINER (for privileged system operations)
--     - INVOKER (for pure predicates and helpers)
--
-- Role access:
-- - app_system:
--     - EXECUTE allowed on non-SECURITY DEFINER functions
--     - EXECUTE allowed on explicitly approved SECURITY DEFINER functions
-- - app_user:
--     - No direct EXECUTE by default
--     - Access granted selectively for safe predicates if required
--
-- RLS interaction:
-- - Predicate functions in this schema are designed to be:
--     - RLS-safe
--     - STABLE
--     - Side-effect free
--
-- Architectural rule:
-- - app_system never mutates tables directly
-- - All system-owned writes must go through functions in this schema
-- - RLS policies must never contain business logic; they may only
--   call predicate functions defined here
--
-- Notes:
-- - This schema represents the execution boundary of the system
-- - App code expresses intent; functions here decide reality
-- - Consistency and correctness take precedence over convenience
-- ------------------------------------------------------------------

-- Create schema for functions owned by admin
CREATE SCHEMA app_fcn
	AUTHORIZATION app_admin;
