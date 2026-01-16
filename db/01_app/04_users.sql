CREATE TABLE IF NOT EXISTS app.users (
    id UUID PRIMARY KEY,

    email CITEXT NOT NULL,
    password_hash TEXT NOT NULL,

    disabled_at timestamptz NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),

    -- unique constraint
    CONSTRAINT uq_users_email
        UNIQUE (email),

    -- check constraint
    CONSTRAINT chk_users_email_not_empty
        CHECK (email <> ''),

    CONSTRAINT chk_users_disable_after_created
        CHECK (disabled_at IS NULL OR disabled_at >= created_at)
);
