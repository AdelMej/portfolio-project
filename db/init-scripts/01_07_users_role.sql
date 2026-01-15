\c app

CREATE TABLE if not exists app.user_roles (
	user_id UUID NOT NULL,
	role_id integer NOT null,
	  
	-- primary key
	CONSTRAINT pk_user_roles
		PRIMARY KEY (user_id, role_id),
	  
	-- foreign keys
	CONSTRAINT fk_user_roles_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id)
		ON DELETE CASCADE,
	  
	CONSTRAINT fk_user_roles_role_id
		FOREIGN KEY (role_id)
		REFERENCES app.roles(id)
		ON DELETE CASCADE
);

COMMENT ON TABLE app.user_roles IS
'Junction table linking users to roles (many-to-many)';
