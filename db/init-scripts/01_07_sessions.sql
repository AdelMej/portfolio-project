\c app

CREATE TABLE IF NOT EXISTS app.sessions (
	id UUID PRIMARY KEY,
	coach_id UUID NOT NULL,
	title varchar(128) NOT NULL,
	start_at timestamptz NOT NULL,
	end_at timestamptz NOT NULL,
	status VARCHAR (16) NOT NULL DEFAULT 'scheduled',
	
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now(),
	
	-- foreign key
	CONSTRAINT fk_sessions_coach_id
		FOREIGN KEY (coach_id)
		REFERENCES app.users(id)
		ON DELETE CASCADE,
		
	-- check constraint
	CONSTRAINT chk_sessions_time_valid
		CHECK (end_at > start_at),
	
	CONSTRAINT chk_sessions_status
		CHECK (status IN ('scheduled', 'cancelled', 'completed'))
)
