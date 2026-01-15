CREATE TABLE IF NOT EXISTS app.user_profiles (
	user_id UUID PRIMARY KEY
		REFERENCES app.users(id)
		ON DELETE CASCADE,

	first_name VARCHAR(100) not null,
	last_name VARCHAR(100) not null,
	
	created_at TIMESTAMPTZ not null default now(),
	updated_at TIMESTAMPTZ not null default now(),
	
	-- constraint
	constraint chk_user_profiles_first_name_not_empty
		check (first_name <> ''),

	constraint chk_user_profiles_last_name_not_empty
		check (last_name <> '')
)