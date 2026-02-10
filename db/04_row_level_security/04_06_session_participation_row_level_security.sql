-- ------------------------------------------------------------------
-- Row Level Security: app.session_participation
--
-- Purpose:
-- - Control visibility and modification of session participation records
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.session_participation ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.session_participation FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: session_participation_select
--
-- Who can see session participation records:
-- 1. Self
-- 2. Coach → participants
-- 3. App-level admin
-- ------------------------------------------------------------------
CREATE POLICY session_participation_select
ON app.session_participation
FOR SELECT
USING (
    ------------------------------------------------------------------
    -- 1. Self
    ------------------------------------------------------------------
    user_id = current_setting('app.current_user_id')::uuid

    OR

    ------------------------------------------------------------------
    -- 2. Coach → participants
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.sessions s
        WHERE s.id = session_participation.session_id
          AND s.coach_id = current_setting('app.current_user_id')::uuid
    )

    OR

    ------------------------------------------------------------------
    -- 3. App-level admin
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
);

COMMENT ON POLICY session_participation_select ON app.session_participation IS
'Allows users to see their own session registrations, coaches to see participants, and admins to see all.';
