-- ------------------------------------------------------------------
-- Role: app_system
--
-- Purpose:
-- - Trusted application system actor
-- - Used by:
--   - background jobs (cron)
--   - webhooks
--   - internal maintenance tasks
--   - lifecycle automation (tokens, cleanup, anonymisation, etc.)
--
-- Security model:
-- - Subject to Row Level Security (NO BYPASSRLS)
-- - Privileges are explicitly granted per-table
-- - Cannot manage schema or roles
--
-- Notes:
-- - NOT used by end users
-- - NOT a database administrator
-- - Application runtime must clearly distinguish app_user vs app_system
-- - All destructive actions must be intentional and scoped
-- ------------------------------------------------------------------

CREATE ROLE app_system
    LOGIN                       -- Allows programmatic login
    PASSWORD 'CHANGE_ME_APP'    -- Placeholder password (rotate immediately)
    NOSUPERUSER                 -- Not a PostgreSQL superuser
    NOCREATEDB                  -- Cannot create databases
    NOCREATEROLE                -- Cannot create or modify roles
    NOREPLICATION               -- No replication privileges
    INHERIT;                    -- Inherits explicitly granted privileges
