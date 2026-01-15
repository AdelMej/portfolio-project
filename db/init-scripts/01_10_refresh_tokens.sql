\c app

CREATE TABLE IF NOT EXISTS app.refresh_tokens(
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY key,
	
	user_id UUID NOT NULL,
	token_hash TEXT NOT null,
	
	created_at timestamptz NOT NULL DEFAULT now(),
	expires_at timestamptz NOT NULL,
	revoked_at timestamptz,
	
	replaced_by_token BIGINT,
	
	-- foreign
	CONSTRAINT fk_refresh_tokens_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id)
		ON DELETE cascade,
		
	-- unique token hash
	CONSTRAINT uq_refresh_tokens_token_hash
		UNIQUE (token_hash),
		
	-- token invariant and revocation rules
	CONSTRAINT chk_refresh_tokens_expiery
		CHECK (expires_at > created_at),

	CONSTRAINT chk_revoked_after_creation
		CHECK (revoked_at IS NULL OR revoked_at >= created_at)
)
