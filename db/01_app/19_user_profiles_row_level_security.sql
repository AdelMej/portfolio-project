-- activating row level security
ALTER TABLE app.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.user_profiles FORCE ROW LEVEL SECURITY;

CREATE POLICY user_profiles_visible
ON app.user_profiles
FOR SELECT
USING (
    -- Self
    app.user_profiles.user_id = current_setting('app.current_user_id')::uuid

    OR

    -- Participant ↔ participant (shared session)
    EXISTS (
        SELECT 1
        FROM app.session_participation sp_target
        JOIN app.session_participation sp_self
          ON sp_self.session_id = sp_target.session_id
        WHERE sp_target.user_id = app.user_profiles.user_id
          AND sp_self.user_id = current_setting('app.current_user_id')::uuid
          AND sp_target.cancelled_at IS NULL
          AND sp_self.cancelled_at IS NULL
    )

    OR

    -- Coach → participant
    EXISTS (
        SELECT 1
        FROM app.sessions s
        JOIN app.session_participation sp
          ON sp.session_id = s.id
        WHERE s.coach_id = current_setting('app.current_user_id')::uuid
          AND sp.user_id = app.user_profiles.user_id
          AND sp.cancelled_at IS NULL
    )

    OR

    -- Participant → coach
    EXISTS (
        SELECT 1
        FROM app.sessions s
        JOIN app.session_participation sp
          ON sp.session_id = s.id
        WHERE s.coach_id = app.user_profiles.user_id
          AND sp.user_id = current_setting('app.current_user_id')::uuid
          AND sp.cancelled_at IS NULL
    )
);

