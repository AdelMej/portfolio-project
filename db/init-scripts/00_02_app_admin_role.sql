-- ------------------------------------------------------------------
-- Role: app_admin
--
-- Purpose:
-- - Database administrator / owner role
-- - Used for schema management, migrations, maintenance, and audits
-- - NOT part of application runtime logic
--
-- Security model:
-- - Bypasses Row Level Security by design
-- - Trusted operational role
-- - Still not a PostgreSQL superuser (controlled blast radius)
--
-- Notes:
-- - Application code MUST NOT connect as this role
-- - Intended for humans, CI migrations, and admin tooling only
-- ------------------------------------------------------------------

CREATE ROLE app_admin
    LOGIN                        -- Allows direct database login
    PASSWORD 'CHANGE_ME_ADMIN'   -- Placeholder password (rotate immediately)
    NOSUPERUSER                  -- Not a PostgreSQL superuser
    CREATEDB                     -- Can create databases
    CREATEROLE                   -- Can create and manage roles
    NOREPLICATION                -- No replication privileges
    BYPASSRLS                    -- Explicitly bypasses all RLS policies
    INHERIT;                     -- Inherits privileges from granted roles
