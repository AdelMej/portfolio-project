CREATE TABLE app.roles(
	id INTEGER GENERATED always AS IDENTITY PRIMARY KEY,

	role_name varchar(64) NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	
	-- constraint
	CONSTRAINT uq_roles_role_name
		UNIQUE (role_name),
	
	CONSTRAINT chk_roles_role_name_not_empty
		CHECK (role_name <> '')
)