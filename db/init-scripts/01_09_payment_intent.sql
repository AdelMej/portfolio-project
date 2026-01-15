\c app

CREATE TABLE IF NOT EXISTS app.payment_intents(
	id UUID PRIMARY key,
	
	user_id UUID NOT null,
	session_id UUID NOT null,
	
	provider TEXT NOT null,
	provider_intent_id TEXT NOT null,
	status TEXT NOT null,

	credit_applied_cents INTEGER NOT NULL DEFAULT 0,
	amount_cents INTEGER NOT null,
	currency CHAR(3) NOT null,
	
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now(),
	
	-- foreign key
	CONSTRAINT fk_payment_intents_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id),
		
	CONSTRAINT fk_payment_intents_session_id
		FOREIGN KEY (session_id)
		REFERENCES app.sessions(id),
		
	-- uniqueness
	CONSTRAINT uq_provider_intent
		UNIQUE (provider, provider_intent_id),
		
	-- checks
	CONSTRAINT chk_payment_intents_provider_not_empty
		check (provider <> ''),
		
	constraint chk_payment_intents_provider_intent_id_not_empty
		check (provider_intent_id <> ''),
		
	constraint chk_payment_intents_status_not_empty
		check (status <> ''),
		
	constraint chk_payment_intents_amount_positive
		check (amount_cents > 0 OR credit_applied_cents > 0),
		
	constraint chk_payment_intents_currency_format
		check (currency ~ '^[A-Z]{3}$'),
		
	CONSTRAINT chk_paymen_t_intent_credit_non_negatvie
		CHECK (credit_applied_cents >= 0)
)