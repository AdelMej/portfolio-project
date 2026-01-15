\c app

CREATE TABLE IF NOT EXISTS app.invite_tokens(
  id UUID PRIMARY key,
  
  token_hash TEXT NOT null,
  
  expires_at timestamptz NOT NULL,
  used_at timestamptz NULL,
  
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by UUID NULL,
  
  -- foreign key
  CONSTRAINT chk_invite_not_used_twice
  	CHECK (used_at IS NOT NULL OR used_at >= created_at)
  	
)
