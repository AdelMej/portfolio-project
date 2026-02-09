\c app

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

COMMENT ON FUNCTION app_fcn.user_exists_by_email(text) IS
'Checks whether a user exists with the given email address. 
Executed as SECURITY DEFINER to bypass RLS for authentication and system-level checks.';
