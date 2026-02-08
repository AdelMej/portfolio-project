-- ------------------------------------------------------------------
-- Privileges: app.session_participation
--
-- Purpose:
-- - Grant access according to role responsibilities
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- app_user: business logic owner
--
-- Notes:
-- - RLS controls which rows are visible and which updates are allowed.
-- - Can register themselves and cancel their own participation.
-- ------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE
ON TABLE app.session_participation
TO app_user;

COMMENT ON TABLE app.session_participation IS
'App users (app_user) may view, register, or cancel their own session participation. RLS governs row visibility and permissible updates.';

-- ------------------------------------------------------------------
-- app_system: read-only
--
-- Notes:
-- - Used for background jobs, metrics, exports.
-- ------------------------------------------------------------------
GRANT SELECT
ON TABLE app.session_participation
TO app_system;

COMMENT ON TABLE app.session_participation IS
'System automation (app_system) may read session participation for reporting and background processing.';

-- ------------------------------------------------------------------
-- app_admin: full control
--
-- Notes:
-- - Database administrators may manage all session participation records.
-- ------------------------------------------------------------------
GRANT ALL
ON TABLE app.session_participation
TO app_admin;

COMMENT ON TABLE app.session_participation IS
'Admins (app_admin) may fully manage session participation records.';
