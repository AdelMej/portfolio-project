-- ------------------------------------------------------------------
-- Table: app.users
--
-- Purpose:
-- - Stores application user identities
-- - Authentication + account lifecycle state
--
-- Design principles:
-- - Email is the primary human identifier
-- - Accounts are never deleted, only disabled
-- - Lifecycle state is explicit and auditable
-- - Business invariants enforced at the database level
--
-- Notes:
-- - Passwords are stored as hashes only
-- - Case-insensitive email via CITEXT
-- - Soft-disable model (disabled_at / disabled_reason)
-- ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app.users (
    -- Primary identifier
    id UUID PRIMARY KEY,

    -- Authentication
    email CITEXT NOT NULL,
    password_hash TEXT NOT NULL,

    -- Account lifecycle
    disabled_at timestamptz NULL,
    disabled_reason TEXT NULL, -- 'self' | 'admin'
    
    -- Timestamps
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),

    -- ------------------------------------------------------------------
    -- Constraints
    -- ------------------------------------------------------------------

    -- Enforce unique email identity (case-insensitive)
    CONSTRAINT uq_users_email
        UNIQUE (email),

    -- Email must not be empty
    CONSTRAINT chk_users_email_not_empty
        CHECK (email <> ''),

    -- Disabled timestamp must not predate creation
    CONSTRAINT chk_users_disable_after_created
        CHECK (disabled_at IS NULL OR disabled_at >= created_at),

    -- disabled_at and disabled_reason must be set together
    CONSTRAINT chk_users_disabled_consistency
        CHECK (
            (disabled_at IS NULL AND disabled_reason IS NULL)
            OR
            (disabled_at IS NOT NULL AND disabled_reason IS NOT NULL)
        ),

    -- Allowed disable reasons
    CONSTRAINT chk_users_disabled_reason
        CHECK (
            disabled_reason IS NULL
            OR disabled_reason IN ('self', 'admin')
        )
);

-- ------------------------------------------------------------------
-- Comments
-- ------------------------------------------------------------------

COMMENT ON TABLE app.users IS
'Application users. Stores authentication identity and account lifecycle state. Users are never deleted; accounts are disabled via disabled_at/disabled_reason.';

COMMENT ON COLUMN app.users.id IS
'Primary user identifier (UUID). Stable, never reused.';

COMMENT ON COLUMN app.users.email IS
'User email address. Case-insensitive (CITEXT). Unique across all users.';

COMMENT ON COLUMN app.users.password_hash IS
'Hashed password (never plaintext). Algorithm determined by application layer.';

COMMENT ON COLUMN app.users.disabled_at IS
'Timestamp when the account was disabled. NULL means the account is active.';

COMMENT ON COLUMN app.users.disabled_reason IS
'Reason for account disablement: self (user-initiated) or admin (administrative action).';

COMMENT ON COLUMN app.users.created_at IS
'Timestamp when the user account was created.';

COMMENT ON COLUMN app.users.updated_at IS
'Timestamp of last modification. Maintained via trigger.';
