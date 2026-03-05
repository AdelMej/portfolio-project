-- ------------------------------------------------------------------
-- Role: app_user
--
-- Purpose:
-- - Represents a regular application user at the database level
-- - Used for all end-user initiated actions
-- - Subject to Row Level Security (RLS) policies
--
-- Security model:
-- - Minimal privileges
-- - No schema or role management
-- - No direct access outside allowed RLS paths
-- ------------------------------------------------------------------

CREATE ROLE app_user
    LOGIN                       -- Allows authentication to the database
    PASSWORD 'CHANGE_ME_APP'    -- Placeholder password (must be rotated)
    NOSUPERUSER                 -- Cannot bypass permissions or RLS
    NOCREATEDB                  -- Cannot create databases
    NOCREATEROLE                -- Cannot create or manage roles
    NOREPLICATION               -- Cannot use replication features
    INHERIT;                    -- Inherits privileges from granted roles
