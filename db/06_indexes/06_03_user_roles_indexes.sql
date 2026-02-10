-- ------------------------------------------------------------------
-- Indexes: app.user_roles
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Role-based lookups
--
-- Used by:
-- - admin role management
-- - permission checks
-- - audit queries by role
--
-- Complements the composite primary key by
-- allowing efficient reverse lookups (role → users)
-- ---------------------------------------------------------------

CREATE INDEX idx_user_roles_role_id
ON app.user_roles (role_id);

COMMENT ON INDEX app.idx_user_roles_role_id IS
'Supports efficient lookups of users by role_id for admin and authorization queries.';
