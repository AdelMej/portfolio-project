\c app

-- ------------------------------------------------------------------
-- Indexes: app.user_profiles
--
-- Purpose:
-- - Speed up name-based lookups (search, admin listing, filters)
-- - Used for directory views and user discovery
-- ------------------------------------------------------------------

-- Fast lookup by last name
CREATE INDEX idx_user_profiles_last_name
ON app.user_profiles (last_name);

COMMENT ON INDEX app.idx_user_profiles_last_name IS
'Speeds up lookups and filtering by user last name (admin search, directories).';

-- Fast lookup by first name
CREATE INDEX idx_user_profiles_first_name
ON app.user_profiles (first_name);

COMMENT ON INDEX app.idx_user_profiles_first_name IS
'Speeds up lookups and filtering by user first name (admin search, directories).';