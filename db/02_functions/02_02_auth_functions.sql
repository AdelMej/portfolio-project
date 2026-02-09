CREATE OR REPLACE FUNCTION app_fcn.auth_exists_by_email(p_email text)
RETURNS boolean
LANGUAGE SQL
SECURITY DEFINER
STABLE
AS $$
	SELECT EXISTS(
		SELECT 1
		FROM app.users u
		WHERE u.email = p_email
	);
$$;

COMMENT ON FUNCTION app_fcn.auth_exists_by_email(text) IS
'Checks whether a user exists with the given email address. 
Executed as SECURITY DEFINER to bypass RLS for authentication and system-level checks.';

create or replace function app_fcn.auth_user_by_email(p_email text)
returns table(
	user_id uuid,
	email text,
	password_hash text,
	disabled_at timestamptz,
	disabled_reason text,
	roles text[]
)
language sql
security definer
stable
as $$
	SELECT
		u.id,
		u.email,
		u.password_hash,
		u.disabled_at,
		u.disabled_reason,
		array_agg(r.role_name ORDER BY r.role_name)
	FROM app.users u
	JOIN app.user_roles ur ON ur.user_id = u.id
	JOIN app.roles r on r.id = ur.role_id
	WHERE u.email = p_email
	GROUP BY
		u.id,
		u.email,
		u.password_hash,
		u.disabled_at,
		u.disabled_reason;
$$;

COMMENT ON FUNCTION app_fcn.auth_user_by_email(text) IS
'Returns authentication-relevant user data and roles for the given email. 
Executed as SECURITY DEFINER to bypass RLS during login and identity verification flows.';

create or replace function app_fcn.create_refresh_token(
	p_user_id uuid,
	p_token_hash text,
	p_expires_at timestamptz
)
returns BIGINT
language sql
security definer
as $$
	insert into app.refresh_tokens (
		user_id,
		token_hash,
		expires_at
	)
	VALUES (
		p_user_id,
		p_token_hash,
		p_expires_at	
	)
	RETURNING id;
$$;

COMMENT ON FUNCTION app_fcn.create_refresh_token(UUID, TEXT, timestamptz) IS
'Creates a refresh token for a user. Bypasses RLS and privilege checks; intended for authentication flows only.';


create or replace function app_fcn.rotate_refresh_token(
	p_new_id bigint,
	p_old_token_hash text,
	p_user_id uuid
)
returns void
language sql
security definer
as $$
	UPDATE app.refresh_tokens
	SET replaced_by_token_id = p_new_id,
		revoked_at = now()
	WHERE token_hash = p_old_token_hash
		AND user_id = p_user_id
		AND revoked_at is null
$$;

COMMENT ON FUNCTION app_fcn.rotate_refresh_token(bigint, TEXT, uuid) IS
'Revokes an existing refresh token and links it to a newly issued token. 
Fails if the token does not exist, is already revoked, or is not owned by the user.';

create or replace function app_fcn.get_active_refresh_token(p_token_hash text)
returns table (
	user_id uuid,
	token_hash text,
	created_at timestamptz,
	expires_at timestamptz,
	revoked_at timestamptz
)
language sql
security definer
stable
as $$
	SELECT
		rt.user_id,
		rt.token_hash,
		rt.created_at,
		rt.expires_at,
		rt.revoked_at
	FROM app.refresh_tokens rt
	WHERE rt.token_hash = p_token_hash
	AND rt.revoked_at is NULL;
$$;

COMMENT ON FUNCTION app_fcn.get_active_refresh_token IS
'Returns an active (non-revoked) refresh token by hash. Returns no rows if the token is invalid or revoked. Does not raise.';


create or replace function app_fcn.register_user(
	p_user_id uuid,
	p_email citext,
	p_password_hash text,
	p_first_name text,
	p_last_name text,
	p_role_name text
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
DECLARE
	v_role_id bigint;
BEGIN
	-- create user
	INSERT INTO app.users(id, email, password_hash)
	VALUES(p_user_id, p_email, p_password_hash);

	-- create profile
	INSERT INTO app.user_profiles(user_id, first_name, last_name)
	VALUES (p_user_id, p_first_name, p_last_name);

	-- resolve role
	SELECT r.id
	into v_role_id
	from app.roles r
	where r.role_name = p_role_name;

	if v_role_id IS NULL then
		RAISE EXCEPTION 'unknown_role'
			USING ERRCODE = 'AP002'; 
	end if;

	-- assign role
	INSERT INTO app.user_roles(user_id, role_id)
	VALUES (p_user_id, v_role_id);

EXCEPTION 
	WHEN unique_violation THEN
		RAISE EXCEPTION 'user_already_exists'
			USING ERRCODE = 'AP001';

END;
$$;

COMMENT ON FUNCTION app_fcn.register_user IS
'Atomic user registration. Inserts user, profile, and role. Raises AP001 (user_already_exists) or AP002 (unknown_role).';


create or replace function app_fcn.auth_user_by_id(p_user_id uuid)
returns table(
	id uuid,
	email text,
	password_hash text,
	disabled_at timestamptz,
	disabled_reason text,
	roles text[]
)
language sql
security definer
stable
as $$
	SELECT
		u.id,
		u.email,
		u.password_hash,
		u.disabled_at,
		u.disabled_reason,
		array_agg(r.role_name) AS roles
	FROM app.users u
	JOIN app.user_roles ur ON u.id = ur.user_id
	JOIN app.roles r ON r.id = ur.role_id
	WHERE u.id = p_user_id
	GROUP BY
		u.id,
		u.email,
		u.password_hash,
		u.disabled_at,
		u.disabled_reason;
$$;

COMMENT ON FUNCTION app_fcn.auth_user_by_id(uuid) IS
'Returns authentication-critical user data by user ID (including roles). Used internally by the system for auth and token workflows. Bypasses RLS. Does not raise.';

create or replace function app_fcn.revoke_all_refresh_token(
	p_user_id uuid
)
returns void
language sql
security definer
as $$
	UPDATE app.refresh_tokens
	SET revoked_at = now()
	where user_id = p_user_id
		AND revoked_at IS NULL
$$;

COMMENT ON FUNCTION app_fcn.revoke_all_refresh_token(uuid) IS
'Revokes all active refresh tokens for a user by setting revoked_at. Used internally for logout-all and security events. Does not raise.';


create or replace function app_fcn.revoke_refresh_token(
	p_token_hash text
)
returns void
language sql
security definer
as $$
	UPDATE app.refresh_tokens
	SET revoked_at = now()
	where token_hash = p_token_hash
		AND revoked_at IS NULL;
$$;

COMMENT ON FUNCTION app_fcn.revoke_refresh_token(text) IS
'Revokes a single refresh token by hash. Used internally for token rotation or explicit logout. Does not raise.';