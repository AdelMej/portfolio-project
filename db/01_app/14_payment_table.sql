CREATE TABLE IF NOT EXISTS app.payment (
	id UUID PRIMARY KEY,
	
	session_id UUID NOT NULL,
	user_id UUID NOT NULL,
	
	provider TEXT NOT NULL,
	provider_payment_id TEXT NOT NULL,
	
	amount_cents INTEGER NOT NULL,
	currency CHAR(3) NOT NULL,
	
	created_at timestamptz NOT NULL DEFAULT now(),
	-- uniqueness ofr idempotency
	CONSTRAINT uq_payment_provider_id
		UNIQUE (provider, provider_payment_id),
		
	-- foreign keys
	CONSTRAINT fk_payment_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id),
		
	CONSTRAINT fk_payment_session_id
		FOREIGN KEY (session_id)
		REFERENCES app.sessions(id),
		
	-- checks
	CONSTRAINT chk_payment_amount_positive
		CHECK (amount_cents > 0),
		
	CONSTRAINT chk_payment_currency_format
		CHECK(currency ~ '^[A-Z]{3}$')
)