CREATE TABLE IF NOT EXISTS app.credit_ledger (
	id UUID PRIMARY key,
	
	user_id UUID NOT NULL,
	payment_intent_id UUID NOT null,
	
	amount_cents INTEGER NOT null,
	-- positive = credit added
	-- negative = credit spent
	
	balance_after_cents INTEGER NOT NULL,
	
	cause TEXT NOT NULL,
	-- 'payment', 'refund', 'session_usage', 'admin_adjustment'
	
	create_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	
	-- foreign key
	CONSTRAINT fk_credit_ledger_user_id
		FOREIGN KEY (user_id)
		REFERENCES app.users(id),
	
	CONSTRAINT fk_credit_ledger_payment_intent_id
		FOREIGN KEY (payment_intent_id)
		REFERENCES app.payment_intents(id),
		
	CONSTRAINT chk_credit_ledger_amount_not_zero
		CHECK (amount_cents <> 0),
		
	CONSTRAINT chk_credit_ledger_balance_not_negative
		CHECK (balance_after_cents >= 0)		
);