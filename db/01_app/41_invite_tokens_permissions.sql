-- ------------------------------------------------------------------
-- Privileges: app.session_participation
--
-- Purpose:
-- - Grant access according to role responsibilities
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: business logic owner
-- ------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE
ON TABLE app.session_participation
TO app_user;

COMMENT ON TABLE app.session_participation IS
'Regular users (app_user) can manage their own session registrations. Row Level Security enforces which rows and updates are allowed.';

-- ------------------------------------------------------------------
-- app_system: read-only (metrics, background jobs, exports)
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.session_participation
TO app_system;

COMMENT ON TABLE app.session_participation IS
'System automation (app_system) can read session participation data for reporting, metrics, or background tasks. RLS still applies.';

-- ------------------------------------------------------------------
-- app_admin: database administrator
-- ------------------------------------------------------------------
GRANT ALL
ON TABLE app.session_participation
TO app_admin;

COMMENT ON TABLE app.session_participation IS
'Admin users (app_admin) have full access to session participation data, bypassing business logic restrictions.';
