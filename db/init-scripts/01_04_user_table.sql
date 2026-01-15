\c app

CREATE TABLE if not exists app.users (
	id UUID primary key,
	
	email CITEXT not null,
	password_hash TEXT not null,
	
	first_name VARCHAR(100) not null,
	last_name VARCHAR(100) not null,

	disabled_at timestamptz null,
	created_at TIMESTAMPTZ not null default now(),
	updated_at TIMESTAMPTZ not null default now(),
	
	-- constraint
	constraint uq_users_email
		unique (email),

	constraint chk_users_email_not_empty
		check (email <> ''),

	constraint chk_users_first_name_not_empty
		check (first_name <> ''),

	constraint chk_users_last_name_not_empty
		check (last_name <> ''),
		
	constraint chk_users_disable_after_created
		check(disabled_at is null or disabled_at >= created_at)
)
