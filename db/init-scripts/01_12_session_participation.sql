 \c app

CREATE TABLE IF NOT EXISTS app.session_participation (
	id UUID PRIMARY KEY,	

	session_id UUID NOT NULL,
	user_id UUID NOT null,
	
	registered_at timestamptz NOT NULL DEFAULT now(),
	cancelled_at timestamptz NULL,
	
	-- unique constraint to prevent double registration
	CONSTRAINT uq_session_participation_user_session
		UNIQUE (session_id, user_id),

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