-- ==================================================================
-- File: 04_02_admin_seed.sql
--
-- Purpose:
-- - Seeds the initial administrator account
-- - Assigns admin role
-- - Creates administrator user profile
--
-- Execution context:
-- - Runs during database initialization
-- - Executed as superuser
-- - Intended to run exactly once
--
-- Notes:
-- - Password hash must be generated externally (Argon2id)
-- - Active account is represented by NULL disabled_at / disabled_reason
-- ==================================================================


-- ------------------------------------------------------------------
-- Seed: Initial administrator user
--
-- Purpose:
-- - Bootstraps system administration access
-- - Provides first login identity
--
-- Notes:
-- - Account starts ACTIVE (not disabled)
-- - UUID generated at insert time
-- ------------------------------------------------------------------
WITH admin_user AS (
    INSERT INTO app.users (
        id,
        email,
        password_hash
    )
    VALUES (
        '00000000-0000-0000-0000-000000000001',
        'admin@example.com',
        '$argon2id$v=19$m=65536,t=3,p=4$UGRYqUO3NS5J8/cKjD09mg$KblEZs8ghdYADYaEwh6EsghQy88rVDpdzEFAWXFswps'
    )
    RETURNING id
),

-- ------------------------------------------------------------------
-- Role resolution
--
-- Purpose:
-- - Resolves admin role dynamically
-- ------------------------------------------------------------------
admin_role AS (
    SELECT id
    FROM app.roles
    WHERE role_name = 'admin'
),

-- ------------------------------------------------------------------
-- User ↔ Role mapping
--
-- Purpose:
-- - Grants admin privileges to bootstrap user
-- ------------------------------------------------------------------
insert_user_role AS (
    INSERT INTO app.user_roles (
        user_id,
        role_id
    )
    SELECT
        au.id,
        ar.id
    FROM admin_user au
    CROSS JOIN admin_role ar
    RETURNING user_id
)

-- ------------------------------------------------------------------
-- Seed: Administrator profile
--
-- Purpose:
-- - Creates required human-facing profile
-- ------------------------------------------------------------------
INSERT INTO app.user_profiles (
    user_id,
    first_name,
    last_name
)
SELECT
    iur.user_id,
    'System',
    'Administrator'
FROM insert_user_role iur;


-- ==================================================================
-- End of admin seed
-- ==================================================================
