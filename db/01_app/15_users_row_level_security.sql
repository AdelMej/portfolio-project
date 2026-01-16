-- Table users
ALTER TABLE app.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.users FORCE ROW LEVEL SECURITY;

-- table users policy
CREATE POLICY users_select_self_or_admin
ON app.users
FOR SELECT
USING (
	id = current_setting('app.current_user_id')::uuid
	OR EXISTS(
		SELECT 1
		FROM app.user_roles ur
		JOIN app.roles r ON r.id = ur.role_id
		WHERE ur.user_id = current_setting('app.current_user_id')::uuid
			AND r.role_name = 'admin'
	)
);

CREATE POLICY users_self_update_profile
ON app.users
FOR UPDATE
USING (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL
)
WITH CHECK (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL
);


CREATE POLICY users_self_delete
ON app.users
FOR UPDATE
USING (
    id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NULL
    AND NOT EXISTS (
	    SELECT 1
	    FROM app.user_roles ur
	    JOIN app.roles r ON r.id = ur.role_id
	    WHERE ur.user_id = current_setting('app.current_user_id')::uuid
	      AND r.role_name = 'admin'
	)
)
WITH CHECK (
	id = current_setting('app.current_user_id')::uuid
    AND disabled_at IS NOT NULL
);


CREATE POLICY users_admin_update_others
ON app.users
FOR UPDATE
USING (
    EXISTS (
        SELECT 1
        FROM app.user_roles ur
        JOIN app.roles r ON r.id = ur.role_id
        WHERE ur.user_id = current_setting('app.current_user_id')::uuid
          AND r.role_name = 'admin'
    )
    AND id <> current_setting('app.current_user_id')::uuid
)
WITH CHECK (TRUE);
