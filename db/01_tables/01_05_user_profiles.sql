-- ------------------------------------------------------------------
-- Table: app.user_profiles
--
-- Purpose:
-- - Stores human-facing profile data for users
-- - Separated from authentication concerns (app.users)
--
-- Design principles:
-- - One-to-one relationship with app.users
-- - Profile data is optional at the system level but enforced once created
-- - Lifecycle is bound to the user account
--
-- Notes:
-- - Profiles are deleted automatically when a user is deleted
-- - No soft-delete: profile existence is subordinate to user existence
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.user_profiles (
    -- One-to-one link to users
    user_id UUID PRIMARY KEY
        REFERENCES app.users(id)
        ON DELETE CASCADE,

    -- Profile information
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- ------------------------------------------------------------------
    -- Constraints
    -- ------------------------------------------------------------------

    -- First name must not be empty
    CONSTRAINT chk_user_profiles_first_name_not_empty
        CHECK (first_name <> ''),

    -- Last name must not be empty
    CONSTRAINT chk_user_profiles_last_name_not_empty
        CHECK (last_name <> '')
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.user_profiles IS
'User profile data (human-facing information). One-to-one with app.users. Deleted automatically when the user account is deleted.';

COMMENT ON COLUMN app.user_profiles.user_id IS
'Primary key and foreign key to app.users. Enforces one profile per user.';

COMMENT ON COLUMN app.user_profiles.first_name IS
'User first name. Must be non-empty.';

COMMENT ON COLUMN app.user_profiles.last_name IS
'User last name. Must be non-empty.';

COMMENT ON COLUMN app.user_profiles.created_at IS
'Timestamp when the profile was created.';

COMMENT ON COLUMN app.user_profiles.updated_at IS
'Timestamp of last profile update. Maintained via trigger.';
