\c app

-- ------------------------------------------------------------------
-- Table: app.roles
--
-- Purpose:
-- - Defines application-level roles (RBAC)
-- - Used to grant permissions via role assignments
--
-- Design principles:
-- - Small, stable lookup table
-- - Role names are immutable identifiers at the application level
-- - No soft-delete: roles are expected to be long-lived
--
-- Notes:
-- - This table does NOT map to PostgreSQL roles
-- - It represents logical application roles (e.g. admin, coach, user)
-- ------------------------------------------------------------------

CREATE TABLE app.roles (
    -- Surrogate primary key
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Application role identifier
    role_name VARCHAR(64) NOT NULL,

    -- Creation timestamp
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- ------------------------------------------------------------------
    -- Constraints
    -- ------------------------------------------------------------------

    -- Ensure role names are unique
    CONSTRAINT uq_roles_role_name
        UNIQUE (role_name),
    
    -- Prevent empty role names
    CONSTRAINT chk_roles_role_name_not_empty
        CHECK (role_name <> '')
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.roles IS
'Application-level roles used for RBAC. Logical roles, not PostgreSQL roles.';

COMMENT ON COLUMN app.roles.id IS
'Surrogate primary key for application roles.';

COMMENT ON COLUMN app.roles.role_name IS
'Unique application role identifier (e.g. admin, coach, user).';

COMMENT ON COLUMN app.roles.created_at IS
'Timestamp when the role was created.';
