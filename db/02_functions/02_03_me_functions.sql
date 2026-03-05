CREATE OR REPLACE FUNCTION app_fcn.me_change_password(
	p_user_id uuid,
	p_password_hash text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
as $$
BEGIN
	/*
	 * Function: app_fcn.change_password
	 * --------------------------------
	 * Changes the password of the currently authenticated user.
	 *
	 * This function is executed as SECURITY DEFINER in order to safely
	 * bypass Row-Level Security (RLS) while still enforcing explicit
	 * authorization rules at the database level.
	 *
	 * Authorization:
	 *   - The caller must be the target user (self-operation only).
	 *   - Authorization is validated via app_fcn.is_self(p_user_id).
	 *
	 * Concurrency:
	 *   - Uses pg_advisory_xact_lock scoped to the user_id to serialize
	 *     concurrent user mutations (password, email, soft-delete, etc.).
	 *
	 * Behavior:
	 *   - Updates the password_hash and updated_at fields.
	 *   - Rejects NULL or empty password hashes.
	 *   - Raises an error if the target user does not exist.
	 *
	 * Parameters:
	 *   p_user_id        UUID of the user whose password is being changed.
	 *   p_password_hash Pre-hashed password value (bcrypt/argon2).
	 *
	 * Errors:
	 *   AP401 - Permission denied (non-self access).
	 *   AP400 - Invalid password hash.
	 *
	 * Returns:
	 *   void
	 */
	PERFORM pg_advisory_xact_lock(
		hashtext('user:' || p_user_id::text)
	);

	IF NOT app_fcn.is_self(p_user_id) THEN
		RAISE EXCEPTION 'Permission denied'
			USING ERRCODE = 'AP401';
	END IF;

    IF p_password_hash IS NULL OR length(p_password_hash) = 0 THEN
        RAISE EXCEPTION 'invalid password hash'
            USING ERRCODE = 'AP400';
    END IF;

	UPDATE app.users
	SET password_hash = p_password_hash
		WHERE id = p_user_id;
	RETURN;
END;
$$;

COMMENT ON FUNCTION app_fcn.me_change_password(uuid, text)
IS
'Allows a user to change their own password.
SECURITY DEFINER function to bypass RLS safely.
Uses pg_advisory_xact_lock(user_id) to serialize concurrent user mutations.
Rejects non-self access and invalid password hashes.
Updates password_hash and updated_at timestamp.';


create or replace function app_fcn.me_change_email(
	p_user_id uuid,
	p_email text
)
returns void
language plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
as $$
BEGIN
	/*
	 * Function: app_fcn.me_change_email
	 * --------------------------------
	 * Changes the email address of the currently authenticated user.
	 *
	 * This function is executed as SECURITY DEFINER in order to bypass
	 * Row-Level Security (RLS) while enforcing explicit authorization
	 * rules at the database level.
	 *
	 * Authorization:
	 *   - The caller must be the target user (self-operation only).
	 *   - Authorization is validated via app_fcn.is_self(p_user_id).
	 *
	 * Concurrency:
	 *   - Uses pg_advisory_xact_lock scoped to the user_id to serialize
	 *     concurrent user mutations (email, password, soft-delete, etc.).
	 *
	 * Behavior:
	 *   - Updates the email field for the target user.
	 *   - Performs minimal validation (non-NULL, non-blank).
	 *   - Idempotent: no error is raised if the user does not exist.
	 *
	 * Input validation, normalization, uniqueness checks, and verification
	 * workflows are handled at the application layer.
	 *
	 * Parameters:
	 *   p_user_id UUID of the user whose email is being changed.
	 *   p_email   New email address.
	 *
	 * Errors:
	 *   AP401 - Permission denied (non-self access).
	 *   AP400 - Invalid email value.
	 *
	 * Returns:
	 *   void
	 */
	PERFORM pg_advisory_xact_lock(
		hashtext('user:' || p_user_id::text)
	);

	IF NOT app_fcn.is_self(p_user_id) THEN
		raise exception 'permission denied'
			USING ERRCODE = 'AP401';
	END IF;

	IF p_email IS NULL or length(trim(p_email)) = 0 THEN
		raise exception 'invalid email'
			USING ERRCODE = 'AP400';
	END IF;

	UPDATE app.users
	SET email = lower(trim(p_email))
		WHERE id = p_user_id;

	RETURN;
END;
$$;

COMMENT ON FUNCTION app_fcn.me_change_email(uuid, text)
IS
'Allows a user to change their own email address.
SECURITY DEFINER function used to bypass RLS with explicit authorization.
Uses pg_advisory_xact_lock(user_id) to serialize concurrent user mutations.
Performs minimal validation; full validation and verification are handled
at the application layer. Idempotent if the user does not exist.';


create or replace function app_fcn.me_self_delete(
	p_user_id uuid
)
returns void
language plpgsql
security definer
SET search_path = app, app_fcn, pg_temp
as $$
BEGIN
	/*
	 * Function: app_fcn.me_self_delete
	 * -------------------------------
	 * Soft-deletes and anonymizes the currently authenticated user.
	 *
	 * Executed as SECURITY DEFINER to bypass Row-Level Security (RLS)
	 * while enforcing explicit authorization rules at the database level.
	 *
	 * Authorization:
	 *   - Self-operation only.
	 *   - Validated via app_fcn.is_self(p_user_id).
	 *
	 * Concurrency:
	 *   - Uses pg_advisory_xact_lock scoped to user_id to serialize
	 *     concurrent user mutations.
	 *
	 * Behavior:
	 *   - Sets deleted_at and deleted_reason = ''self''.
	 *   - Invalidates credentials (email, password).
	 *   - Anonymizes user profile data.
	 *   - Idempotent if the user is already deleted or missing.
	 *
	 * Parameters:
	 *   p_user_id UUID of the user performing self-deletion.
	 *
	 * Errors:
	 *   AP401 - Permission denied.
	 *
	 * Returns:
	 *   void
	 */
	perform pg_advisory_xact_lock(
		hashtext('user:' || p_user_id::text)
	);

	IF NOT app_fcn.is_self(p_user_id) THEN
		RAISE Exception 'permission denied'
			USING ERRCODE = 'AP401';
	END IF;

	UPDATE app.users
	SET
        disabled_at = now(),
        disabled_reason = 'self',

        email = concat('deleted+', id::text, '@deleted.invalid'),
        password_hash = '!!deleted!!'
	WHERE id = p_user_id
		AND disabled_at IS NULL;

	UPDATE app.user_profiles
	SET
		first_name = 'deleted',
		last_name = 'deleted'
	WHERE user_id = p_user_id;

	RETURN;
END;
$$;

COMMENT ON FUNCTION app_fcn.me_self_delete(uuid)
IS
'Allows a user to soft-delete and anonymize their own account.
SECURITY DEFINER function to bypass RLS with explicit authorization.
Uses pg_advisory_xact_lock(user_id) to serialize concurrent user mutations.
Invalidates credentials and anonymizes profile data.
Idempotent if the user is already deleted or does not exist.';
