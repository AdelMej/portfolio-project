-- Active users (main runtime path)
CREATE INDEX idx_users_active
ON app.users (id)
WHERE disabled_at IS NULL;

-- Admin listing / audits
CREATE INDEX idx_users_created_at
ON app.users (created_at DESC);

-- Optional: disabled users lookup
CREATE INDEX idx_users_disabled_at
ON app.users (disabled_at)
WHERE disabled_at IS NOT NULL;