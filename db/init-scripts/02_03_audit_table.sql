\c audit

CREATE TABLE IF NOT EXISTS audit.events (
	id BIGINT GENERATED ALWAYS AS IDENTITY,
	occurred_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
	
	actor_type TEXT NOT NULL,    -- 'stripe', 'user', 'system'
	actor_id uuid NULL,          -- nullable for system events
	
	event_type    TEXT NOT NULL, -- SESSION_CREATED, USER_DISABLED
	target_id     UUID NULL,     -- the thing affected
	
	metadata JSONB NOT NULL DEFAULT '{}'
)
