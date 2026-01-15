\c app

CREATE TABLE IF NOT EXISTS app.session_participants (
	session_id UUID NOT NULL,
	user_id UUID NOT null,
	
	registered_at timestamptz NOT NULL DEFAULT now(),

	-- primary key
	CONSTRAINT pk_session_participants
		PRIMARY KEY (session_id, user_id),
		
	-- foreign key
	CONSTRAINT fk_session_participants_session_id
		FOREIGN KEY (session_id)
		REFERENCES app.sessions(id)
		ON DELETE cascade,
		
	CONSTRAINT fk_session_participants_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id)
		ON DELETE CASCADE
)
