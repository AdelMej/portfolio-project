-- ------------------------------------------------------------------
-- Core RLS Authorization Predicates
--
-- Purpose:
-- - Provide minimal, reusable authorization predicates for RLS
-- - Define *who the current user is allowed to act as*
-- - Serve as the foundation for all access-control policies
--
-- Design principles:
-- - Pure predicates: no side effects, no mutations
-- - Evaluated per-row by PostgreSQL RLS engine
-- - Fail-fast if session context is missing or invalid
-- - Composable: intended to be combined by higher-level predicates
--
-- Scope:
-- - Authorization only (no business or domain state)
-- - Answer questions of the form:
--     - "Am I this user?"
--     - "Do I have this role?"
--
-- Dependencies:
-- - Session context (app.current_user_id)
-- - Authorization tables (user_roles, roles)
--
-- Usage:
-- - Used directly inside RLS USING / WITH CHECK clauses
-- - Used indirectly by domain predicates and system functions
--
-- Security model:
-- - Located in app_fcn schema
-- - Never SECURITY DEFINER
-- - Execute with caller privileges
-- - No privilege escalation
--
-- Invariants:
-- - These predicates define the authorization surface of the system
-- - Changes here affect all RLS policies and must be reviewed carefully
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION app_fcn.is_user_active(target_user_id uuid)
RETURNS boolean
LANGUAGE SQL
STABLE
AS $$
	SELECT EXISTS (
		SELECT 1
		FROM app.users u
		WHERE u.id = target_user_id
			AND u.disabled_at IS NULL	
	)
$$;

COMMENT ON FUNCTION app_fcn.is_user_active(uuid) IS
'User domain predicate. Returns true if the specified user exists and is active (not disabled). Centralizes the user lifecycle invariant used by RLS and domain logic.';

CREATE OR REPLACE FUNCTION app_fcn.is_self(p_user_id uuid)
RETURNS boolean
LANGUAGE SQL
STABLE
AS $$
	SELECT
		p_user_id = current_setting('app.current_user_id')::uuid
$$;

COMMENT ON FUNCTION app_fcn.is_self(uuid) IS
'Authorization predicate. Returns true if the target user id matches the current authenticated user. Used for self-access checks in RLS.';

CREATE OR REPLACE FUNCTION app_fcn.is_admin()
RETURNS boolean
LANGUAGE SQL
STABLE
AS $$
	SELECT EXISTS (
		SELECT 1
		FROM app.user_roles ur
		JOIN app.roles r ON r.id = ur.role_id
		WHERE ur.user_id = current_setting('app.current_user_id')::uuid
			AND r.role_name = 'admin'
	)
$$;

COMMENT ON FUNCTION app_fcn.is_admin() IS
'Authorization predicate. Returns true if the current authenticated user has the admin role. Used to gate admin-level access.';

CREATE OR REPLACE FUNCTION app_fcn.is_coach()
RETURNS boolean
LANGUAGE SQL
STABLE
AS $$
	SELECT EXISTS (
		SELECT 1
		FROM app.user_roles ur
		JOIN app.roles r ON ur.role_id = r.id
		WHERE ur.user_id = current_setting('app.current_user_id')::uuid
			AND r.role_name = 'coach'
	)
$$;

COMMENT ON FUNCTION app_fcn.is_coach() IS
'Authorization predicate. Returns true if the current authenticated user has the coach role. Grants coach-level capabilities; does not imply ownership of any session.';


CREATE OR REPLACE FUNCTION app_fcn.current_actor_id()
RETURNS uuid
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
    /*
     * app_fcn.current_actor_id
     *
     * Returns the UUID of the current authenticated actor
     * from the database execution context.
     *
     * Source:
     *   - Reads from the session-scoped setting:
     *       app.current_actor_id
     *
     * Behavior:
     *   - Returns NULL if the setting is not present
     *   - Does not raise on missing context
     *
     * Intended usage:
     *   - Authorization checks inside SECURITY DEFINER functions
     *   - Audit attribution (created_by, coach_id, etc.)
     *   - RLS policies and domain predicates
     *
     * Security:
     *   - SECURITY DEFINER to allow controlled access to
     *     application context regardless of caller role
     *
     * Stability:
     *   - STABLE: value is constant for the duration of a statement
     */
    SELECT current_setting('app.current_actor_id', true)::uuid;
$$;

COMMENT ON FUNCTION app_fcn.current_actor_id() IS
'Returns the UUID of the current authenticated actor from the session-scoped
application setting app.current_actor_id. Intended for use inside SECURITY
DEFINER functions, authorization predicates, auditing, and RLS policies.
Returns NULL if no actor context is present.';


