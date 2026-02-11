CREATE OR REPLACE function app_fcn.admin_user_revoke_role(
	p_role_name text,
	p_target_id uuid
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('user:' || p_target_id::text || ':role:' || p_role_name)
		);
	
		IF NOT app_fcn.is_admin() THEN
			RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
		END IF;
	
		DELETE FROM app.user_roles ur
		USING app.roles r
		WHERE ur.role_id = r.id
			AND ur.user_id = p_target_id
			AND r.role_name = p_role_name;

		RETURN;
	END;
$$;

COMMENT ON FUNCTION app_fcn.admin_user_revoke_role(text, uuid)
IS
'Revokes a role from a target user.
Uses pg_advisory_xact_lock scoped to (user_id, role_name) to serialize concurrent
grant/revoke operations and prevent race conditions under spam or parallel requests.
Idempotent: revoking a non-existing role is a no-op.
Requires admin privileges (checked via app_fcn.is_admin()).';


create or replace function app_fcn.admin_user_grant_role(
	p_role_name text,
	p_target_id uuid
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('user:' || p_target_id::text || ':role:' || p_role_name)
		);

		IF NOT app_fcn.is_admin() THEN
			RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
		END IF;	

		INSERT INTO app.user_roles(user_id, role_id)
		SELECT p_target_id, r.id
		FROM app.roles r
		WHERE r.role_name = p_role_name
			AND NOT EXISTS (
				SELECT 1
				FROM app.user_roles ur
					WHERE ur.user_id = p_target_id
					AND ur.role_id = r.id
			);

		RETURN;
	END;
$$;

COMMENT ON FUNCTION app_fcn.admin_user_grant_role(text, uuid)
IS
'Grants a role to a target user.
Concurrency-safe via pg_advisory_xact_lock scoped to (user_id, role_name) to serialize
grant/revoke operations and prevent race conditions.
Idempotent: granting an already assigned role is a no-op.
Requires admin privileges (checked via app_fcn.is_admin()).';


create or replace function app_fcn.admin_user_disable_user(
	p_target_id uuid
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('user:' || p_target_id::text)
		);
	
		IF NOT app_fcn.is_admin() THEN
			RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
		END IF;

		UPDATE app.users
		SET
			disabled_at = now(),
			disabled_reason = 'admin'
		WHERE id = p_target_id
			AND disabled_at IS NULL;

		RETURN;
	END;
$$;

COMMENT ON FUNCTION app_fcn.admin_user_disable(uuid)
IS
'Admin-only function to disable a user account.
Uses pg_advisory_xact_lock(user_id) to serialize user mutations.
Idempotent: disabling an already disabled user is a no-op.
Sets disabled_at timestamp and disabled_reason.';


create or replace function app_fcn.admin_user_enable_user(
	p_target_id uuid
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('user:' || p_target_id::text)
		);

		IF NOT app_fcn.is_admin() THEN
			RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
		END IF;
	
		UPDATE app.users
		SET
			disabled_at = NULL,
			disabled_reason = NULL
		WHERE id = p_target_id
			AND disabled_at IS NOT NULL
			AND disabled_reason = 'admin';

		RETURN;
	END;
$$;

COMMENT ON FUNCTION app_fcn.enable_user(uuid)
IS
'Admin-only function to re-enable a user account.
Uses pg_advisory_xact_lock(user_id) to serialize user mutations.
Idempotent: enabling an already enabled user is a no-op.
Only re-enables users disabled by admin (disabled_reason = ''admin'').';
