INSERT INTO app.roles(role_name)
VALUES
	('admin'),
	('coach'),
	('user')
ON CONFLICT (role_name) DO NOTHING;