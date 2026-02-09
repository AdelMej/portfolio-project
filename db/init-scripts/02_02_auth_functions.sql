\c app

CREATE OR REPLACE FUNCTION app_fcn.auth_exists_by_email(p_email text)
RETURNS boolean
LANGUAGE SQL
SECURITY DEFINER
STABLE
AS $$
	/*
	Function:
	- auth_exists_by_email
	
	Purpose:
	- Check whether a user exists for a given email
	
	Behavior:
	- Returns true if at least one user exists
	- Returns false otherwise
	- Never raises
	
	Security:
	- SECURITY DEFINER
	- Bypasses RLS for authentication and system checks
	*/
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
	/*
	Function:
	- auth_user_by_email
	
	Purpose:
	- Load authentication-critical user data by email
	
	Behavior:
	- Returns one row if user exists
	- Returns zero rows if not found
	- Aggregates user roles
	- Does not raise
	
	Security:
	- SECURITY DEFINER
	- Bypasses RLS during login and identity verification
	*/
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
	/*
	Function:
	- create_refresh_token
	
	Purpose:
	- Persist a new refresh token for a user
	
	Behavior:
	- Inserts a refresh token row
	- Returns the generated token ID
	- Relies on DB constraints for integrity
	
	Security:
	- SECURITY DEFINER
	- Bypasses RLS and table privileges
	- Intended for authentication flows only
	*/
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
	/*
	Function:
	- rotate_refresh_token
	
	Purpose:
	- Revoke an existing refresh token and link it to a new one
	
	Behavior:
	- Marks the old token as revoked
	- Sets replaced_by_token_id
	- No-op if token is missing, revoked, or not owned by user
	
	Security:
	- SECURITY DEFINER
	- Used internally during token rotation
	*/
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
	/*
	Function:
	- get_active_refresh_token
	
	Purpose:
	- Fetch an active (non-revoked) refresh token by hash
	
	Behavior:
	- Returns one row if token is valid
	- Returns zero rows if revoked or missing
	- Does not raise
	
	Security:
	- SECURITY DEFINER
	- Bypasses RLS for token validation
	*/
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
	/*
	Function:
	- register_user
	
	Purpose:
	- Atomically register a new user account
	
	Behavior:
	- Inserts user, profile, and role mapping
	- Raises AP001 if user already exists
	- Raises AP002 if role is unknown
	
	Security:
	- SECURITY DEFINER
	- Explicit search_path to avoid hijacking
	*/
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
	/*
	Function:
	- auth_user_by_id
	
	Purpose:
	- Load authentication-critical user data by user ID
	
	Behavior:
	- Returns one row if user exists
	- Returns zero rows otherwise
	- Aggregates roles
	- Does not raise
	
	Security:
	- SECURITY DEFINER
	- Used internally for auth and token workflows
	*/
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
	/*
	Function:
	- revoke_all_refresh_token
	
	Purpose:
	- Revoke all active refresh tokens for a user
	
	Behavior:
	- Sets revoked_at on all non-revoked tokens
	- Idempotent
	- Does not raise
	
	Security:
	- SECURITY DEFINER
	- Used for logout-all and security events
	*/
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
	/*
	Function:
	- revoke_refresh_token
	
	Purpose:
	- Revoke a single refresh token by hash
	
	Behavior:
	- Marks token as revoked if active
	- No-op if already revoked or missing
	- Does not raise
	
	Security:
	- SECURITY DEFINER
	- Used for logout and token rotation
	*/
	UPDATE app.refresh_tokens
	SET revoked_at = now()
	where token_hash = p_token_hash
		AND revoked_at IS NULL;
$$;

COMMENT ON FUNCTION app_fcn.revoke_refresh_token(text) IS
'Revokes a single refresh token by hash. Used internally for token rotation or explicit logout. Does not raise.';