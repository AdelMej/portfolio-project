-- ------------------------------------------------------------------
-- Row Level Security: app.user_profiles (optimized)
--
-- Visibility model:
-- - Admins see everything
-- - Users see themselves
-- - Participants see other participants in shared sessions
-- - Coaches see their participants
-- - Participants see their coach
-- ------------------------------------------------------------------

-- Enable and enforce RLS
ALTER TABLE app.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.user_profiles FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------
-- Policy: user_profiles_visible (optimized for performance)
--
-- Who can SELECT user profiles:
-- 1. App-level admins (full visibility)
-- 2. Self
-- 3. Participant ↔ participant (shared active session)
-- 4. Coach → participant
-- 5. Participant → coach
--
-- Notes:
-- - Uses indexed subqueries for large-scale performance
-- - Relies on partial indexes on session_participation:
--     - (user_id) WHERE cancelled_at IS NULL
--     - (session_id) WHERE cancelled_at IS NULL
-- ------------------------------------------------------------------
CREATE POLICY user_profiles_visible
ON app.user_profiles
FOR SELECT
USING (

    ------------------------------------------------------------------
    -- 1. App-level admin: full visibility
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )

    OR

    ------------------------------------------------------------------
    -- 2. Self
    ------------------------------------------------------------------
    user_id = current_setting('app.current_user_id')::uuid

    OR

    ------------------------------------------------------------------
    -- 3. Participant ↔ participant
    --    Users sharing at least one active session
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.session_participation sp_target
        WHERE sp_target.user_id = user_id
          AND sp_target.cancelled_at IS NULL
          AND sp_target.session_id IN (
              SELECT sp_self.session_id
              FROM app.session_participation sp_self
              WHERE sp_self.user_id = current_setting('app.current_user_id')::uuid
                AND sp_self.cancelled_at IS NULL
          )
    )

    OR

    ------------------------------------------------------------------
    -- 4. Coach → participant
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.session_participation sp
        WHERE sp.user_id = user_id
          AND sp.cancelled_at IS NULL
          AND sp.session_id IN (
              SELECT s.id
              FROM app.sessions s
              WHERE s.coach_id = current_setting('app.current_user_id')::uuid
          )
    )

    OR

    ------------------------------------------------------------------
    -- 5. Participant → coach
    ------------------------------------------------------------------
    EXISTS (
        SELECT 1
        FROM app.sessions s
        WHERE s.coach_id = user_id
          AND s.id IN (
              SELECT sp.session_id
              FROM app.session_participation sp
              WHERE sp.user_id = current_setting('app.current_user_id')::uuid
                AND sp.cancelled_at IS NULL
          )
    )
);

COMMENT ON POLICY user_profiles_visible ON app.user_profiles IS
'Controls visibility of user profiles based on shared sessions, coaching relationships, self-access, and admin privileges. Optimized with indexed subqueries for performance.';

-- ------------------------------------------------------------------
-- Policy: user_profiles_self_update
--
-- Users may update ONLY their own profile
-- ------------------------------------------------------------------
CREATE POLICY user_profiles_self_update
ON app.user_profiles
FOR UPDATE
TO app_user
USING (
    user_id = current_setting('app.current_user_id')::uuid
    AND EXISTS (
        SELECT 1
        FROM app.users u
        WHERE u.id = user_profiles.user_id
          AND u.disabled_at IS NULL
    )
)
WITH CHECK (
    user_id = current_setting('app.current_user_id')::uuid
);

COMMENT ON POLICY user_profiles_self_update ON app.user_profiles IS
'Allows users to update only their own profile.';

-- ------------------------------------------------------------------
-- Policy: user_profiles_system_insert
--
-- Only system role may create profiles
-- (signup, sync, migrations, etc.)
-- ------------------------------------------------------------------
CREATE POLICY user_profiles_system_insert
ON app.user_profiles
FOR INSERT
TO app_system
WITH CHECK (TRUE);

COMMENT ON POLICY user_profiles_system_insert ON app.user_profiles IS
'Restricts profile creation to system-level processes.';
