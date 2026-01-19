\c app

-- ------------------------------------------------------------------
-- Row Level Security: app.sessions
--
-- Purpose:
-- - Control who can create and modify sessions
-- - Allow public visibility of session listings
--
-- Guarantees:
-- - All users can view sessions
-- - Only coaches can create their own sessions
-- - Only the owning coach or an admin can update a session
-- - DELETE is intentionally forbidden
-- ------------------------------------------------------------------

-- ------------------------------------------------------------------
-- Enable RLS
-- ------------------------------------------------------------------

ALTER TABLE app.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.sessions FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: public read access
--
-- Everyone may view sessions.
-- Used for:
-- - session listings
-- - discovery
-- - registration flows
-- ------------------------------------------------------------------

CREATE POLICY sessions_select_all
ON app.sessions
FOR SELECT
USING (true);

COMMENT ON POLICY sessions_select_all ON app.sessions IS
'Allows all users to read session data.';

-- ------------------------------------------------------------------
-- Policy: coach creates own sessions
--
-- A coach may only insert sessions where they are the coach.
-- ------------------------------------------------------------------

CREATE POLICY sessions_coach_insert
ON app.sessions
FOR INSERT
TO app_user
WITH CHECK (
    coach_id = current_setting('app.current_user_id')::uuid
);

COMMENT ON POLICY sessions_coach_insert ON app.sessions IS
'Allows a coach to create sessions they own.';

CREATE POLICY sessions_coach_or_admin_update
ON app.sessions
FOR UPDATE
TO app_user
USING (
    -- coach updating their own session
    coach_id = current_setting('app.current_user_id')::uuid

    OR

    -- app-level admin
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
)
WITH CHECK (
    -- same condition: updater must still be coach or admin
    coach_id = current_setting('app.current_user_id')::uuid
    OR
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);


COMMENT ON POLICY sessions_coach_or_admin_update ON app.sessions IS
'Allows session updates by the owning coach or an admin; ownership is immutable.';
