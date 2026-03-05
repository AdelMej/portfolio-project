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
    app_fcn.is_admin()

    OR

    ------------------------------------------------------------------
    -- 2. Self
    ------------------------------------------------------------------
    app_fcn.is_self(user_id)

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
    app_fcn.is_self(user_id)
    AND app_fcn.is_user_active(user_id)
)
WITH CHECK (
    app_fcn.is_self(user_id)
);

COMMENT ON POLICY user_profiles_self_update ON app.user_profiles IS
'Allows users to update only their own profile.';
