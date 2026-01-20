\c app

-- ------------------------------------------------------------------
-- Table: app.user_roles
--
-- Purpose:
-- - Links users to application roles (many-to-many)
-- - Core of RBAC authorization model
--
-- Design principles:
-- - Pure junction table
-- - Append-only by convention (role removals are explicit deletes)
-- - No surrogate key: composite PK enforces uniqueness
--
-- Notes:
-- - Deleting a user cascades and removes all role assignments
-- - Roles themselves are protected from deletion if still assigned
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.user_roles (
    -- User being assigned a role
    user_id UUID NOT NULL,

    -- Role being assigned
    role_id INTEGER NOT NULL,

    -- Timestamp when the role was granted
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- ------------------------------------------------------------------
    -- Primary key
    -- ------------------------------------------------------------------

    -- Prevent duplicate role assignments per user
    CONSTRAINT pk_user_roles
        PRIMARY KEY (user_id, role_id),
      
    -- ------------------------------------------------------------------
    -- Foreign keys
    -- ------------------------------------------------------------------

    -- User reference (cascade on user deletion)
    CONSTRAINT fk_user_roles_user_id
        FOREIGN KEY (user_id)
        REFERENCES app.users(id)
        ON DELETE CASCADE,
      
    -- Role reference (roles cannot be deleted while in use)
    CONSTRAINT fk_user_roles_role_id
        FOREIGN KEY (role_id)
        REFERENCES app.roles(id)
        ON DELETE RESTRICT
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.user_roles IS
'Junction table linking users to application roles (many-to-many).';

COMMENT ON COLUMN app.user_roles.user_id IS
'User receiving the role.';

COMMENT ON COLUMN app.user_roles.role_id IS
'Application role assigned to the user.';

COMMENT ON COLUMN app.user_roles.assigned_at IS
'Timestamp when the role was assigned to the user.';
