# Database Design & Security

## Principles

- Least privilege
- RLS as the primary access control
- No hard deletes
- All invariants enforced at DB level

---

## Roles (DB)

- [app_admin](./00_bootstrap/02_app_admin_role.sql)
- [app_user](./00_bootstrap/01_app_user_role.sql)
- [app_system](./00_bootstrap/03_app_system_role.sql)

---

## Tables

## `app.users`

### Purpose

- Authentication identity table
- Represents a system user
- Users are **never hard-deleted**
- Account lifecycle is managed via `disabled_at`

---

### Lifecycle rules

- Users start **active** (`disabled_at IS NULL`)
- Soft deletion = setting `disabled_at`
- Re-enabling a user = setting `disabled_at` back to `NULL`
- Hard deletes are **not allowed**

---

### Invariants

- A disabled user is immutable
- Users may modify **only their own row**
- Soft deletion is **self-initiated only**
- Admins **cannot** soft-delete themselves
- Admins may disable or re-enable **other users**
- Admins may **not** modify non-lifecycle fields of other users
- No role may hard-delete a user

---

### Row Level Security (RLS)

#### Read access

- Users can read their own row
- Admins can read all users

#### Update access

##### Self update (all users, including admins)

- Allowed only if:
  - user is active
- Scope:
  - full row update allowed
- Restrictions:
  - `disabled_at` may **not** be set by admins on themselves

##### Self delete (non-admin users only)

- Allowed only if:
  - user is active
  - user is **not** an admin
- Result:
  - `disabled_at` must be set
- Restrictions:
  - no other columns may be modified

##### Admin update (other users only)

- Allowed scope:
  - `disabled_at` only
- Intended use:
  - disable users
  - re-enable users
- Restrictions:
  - this path applies only to updates on other users
  - admins updating their own account follow self-update restrictions
  - admins cannot modify any other column on other users

---

### Delete behavior

- `DELETE` is not permitted
- All deletions are implemented as soft deletes via `UPDATE`

---

### Enforcement notes

- All lifecycle rules are enforced at the **database level**
- RLS defines **who** may act
- Triggers enforce **what** may change
- Disabled users cannot be modified by any role
- Application code **cannot bypass** these rules
- Admin self-lockout is explicitly prevented

---

### Relevant scripts

- [Table definition](./01_app/04_users.sql)
- [Row level security](./01_app/16_users_row_level_security.sql)
- [Permissions](./01_app/17_users_permission.sql)
- [Indexes](./01_app/18_users_indexes.sql)
- [Triggers](./01_app/19_users_triggers.sql)

---

## `app.user_profiles`

### Purpose

- Stores user-facing profile information
- Decoupled from authentication and account lifecycle
- Used for display, discovery, and session-related visibility

---

### Lifecycle rules

- Profiles are created **once** at user creation time
- Profiles are **never deleted**
- No soft-delete mechanism exists for profiles
- Profile ownership (`user_id`) never changes

---

### Invariants

- Exactly one profile per user
- `user_id` is immutable
- Profiles cannot be hard-deleted
- Profiles cannot be soft-deleted
- `updated_at` is always system-managed
- Users may only modify their own profile
- Admins may **not** modify other users’ profiles

---

### Row Level Security (RLS)

#### Read access

A profile is visible if **any** of the following is true:

- User is reading their own profile
- Users share at least one active session (participant ↔ participant)
- Coach can read participant profiles for their sessions
- Participant can read their coach’s profile

#### Update access

- **Self update**
  - Users may update **only their own** profile
  - `user_id` must remain unchanged
  - `updated_at` is automatically set

- **Admin update**
  - Admins may update **their own profile only**
  - Admins cannot update other users’ profiles

#### Insert access

- Profiles may only be created by the system role
- Application roles cannot insert profiles directly

---

### Delete behavior

- `DELETE` is not permitted
- Profiles are permanent records

---

### Relevant scripts

- [Table definition](./01_app/05_user_profiles.sql)
- [Row level security](./01_app/20_user_profiles_row_level_security.sql)
- [Permissions](./01_app/21_user_profiles_permissions.sql)
- [Triggers](./01_app/22_user_profiles_indexes.sql)

---

### Notes

- All visibility rules are enforced via RLS
- Application code cannot bypass profile access rules
- Profile privacy is derived exclusively from session relationships
- Admin restrictions are intentional to prevent privilege overreach

---

## `app.roles`

### Purpose

- Defines **application-level roles**
- Used for authorization logic (via `app.user_roles`)
- Represents **fixed semantic roles** (e.g. `admin`, `coach`, `user`)
- Acts as a **lookup / reference table**

---

### Lifecycle rules

- Roles are **created intentionally** (typically via migrations or seeds)
- Roles are **not expected to change**
- Roles are **never soft-deleted or hard-deleted**
- Modifications are considered **schema-level changes**

---

### Invariants

- `role_name` is:
  - unique
  - non-empty
  - immutable by convention
- Each role has a stable identifier
- Roles are referenced by `app.user_roles`
- No business logic depends on role ordering

---

### Access & Security

- No Row Level Security (RLS)
- Roles are not user-owned
- Roles do not contain sensitive data
- Access is controlled indirectly through `app.user_roles`

---

### Indexes

- Unique index on `role_name`
  - Enforced via `UNIQUE (role_name)`
  - Used for fast role lookup during authorization checks

---

### Delete behavior

- Deletion is **not supported**
- Roles must not be removed once referenced
- Role removal requires a **schema migration**

---

### Relevant scripts

- [Table definition](./01_app/06_roles.sql)
- [Permissions](./01_app/24_roles_permissions.sql)

---

### Notes

- Roles are intentionally simple and static
- Authorization logic should **never rely on hardcoded role IDs**
- Role semantics are enforced by:
  - database constraints
  - RLS on dependent tables
- This table is safe to expose read-only at the application level

---

## `app.user_roles`

### Purpose

- Junction table linking users to application roles
- Defines **authorization** at the application level
- Many-to-many relationship between users and roles
- Role assignments are **explicit and auditable**

---

### Lifecycle rules

- Roles are granted via `INSERT`
- Roles are revoked via `DELETE`
- Users are **never hard-deleted**, so role cleanup via cascade is not relied upon
- Role assignments are managed explicitly

---

### Invariants

- A user may have multiple roles
- A role may be assigned to multiple users
- Role assignments are unique per `(user_id, role_id)`
- Users may view **only their own** role assignments
- Admins may grant or revoke roles for **other users**
- Admins **cannot revoke their own admin role**
- `app_system` may grant or revoke roles without restriction

---

### Row Level Security (RLS)

#### Read access

- Users may read their **own** role assignments
- Admins may read **all** role assignments

#### Write access

- **Insert (grant role)**
  - Allowed for:
    - application-level admins
    - `app_system`
  - Not allowed for regular users

- **Delete (revoke role)**
  - Allowed for:
    - application-level admins
    - `app_system`
  - Admins cannot revoke **their own** admin role
  - Revoking roles from other admins is allowed

---

### Delete behavior

- Role revocation is done via `DELETE`
- No hard deletes of users are required or expected
- Safety rules prevent accidental admin lockout

---

### Relevant scripts

- [Table definition](./01_app/07_users_role.sql)
- [Row level security](./01_app/25_user_roles_row_level_security.sql)
- [Permissions](./01_app/26_user_roles_permissions.sql)
- [Indexes](./01_app/27_user_roles_indexes.sql)

---

### Notes

- All authorization rules are enforced at the database level
- Application code cannot bypass role safety constraints
- `app_system` exists for controlled automation and recovery

---

## `app.sessions`

### Purpose

- Core scheduling entity
- Represents a coach-led session that users may join
- Acts as the business anchor for participation and payments

---

### Lifecycle rules

- Sessions are created in `scheduled` state
- Sessions may transition to:
  - `cancelled`
  - `completed`
- Sessions are **never hard-deleted**

---

### Invariants

- `end_at` must be strictly after `start_at`
- A session always has exactly one coach
- Session time range is immutable after creation
- Status transitions are controlled
- Hard deletes are not permitted

---

### Row Level Security (RLS)

#### Read access

- Users may read sessions they are allowed to see
- Coaches may read sessions they own
- Admins may read all sessions

#### Write access

- **Coach**
  - May create sessions
  - May update their own sessions
  - May cancel their own sessions

- **Admin**
  - May update or cancel any session
  - May not create sessions

- **Regular users**
  - Read-only access
  - No direct modification allowed

---

### Delete behavior

- `DELETE` is not permitted
- Session cancellation is represented via `status = 'cancelled'`

---

### Relevant scripts

- [Table definition](./01_app/08_sessions.sql)
- [Row level security](./01_app/28_sessions_row_level_security.sql)
- [Permissions](./01_app/29_sessions_permissions.sql)
- [Indexes](./01_app/30_sessions_indexes.sql)
- [Triggers](./01_app/31_sessions_triggers.sql)

---

### Notes

- Session visibility is further constrained by participation rules
- Business logic is enforced at the database level
- Application code cannot bypass scheduling invariants

---

## `app.payment_intents`

### Purpose

- Stores payment intent state from external payment providers (e.g. Stripe)
- Acts as the **source of truth** for payment lifecycle
- Used by webhook handlers to reconcile payments
- Links a user payment to a specific session

---

### Core concepts

- A payment intent is **created once** and then updated over time
- Identity is defined by `(provider, provider_intent_id)`
- The database enforces immutability and valid state transitions
- Business logic is split:
  - Provider decides payment outcome
  - Database enforces invariants

---

### Invariants

- Payment intents are **never deleted**
- Core fields are immutable after creation:
  - `user_id`
  - `session_id`
  - `provider`
  - `provider_intent_id`
  - `amount_cents`
  - `currency`
- `amount_cents` must be strictly positive
- `credit_applied_cents` must be non-negative
- Currency must be a valid ISO-4217 code (`AAA` format)

---

### Status lifecycle

- Status is provider-driven and stored as text
- Status transitions are **forward-only**
- Terminal states:
  - `succeeded`
  - `canceled`
  - `failed`
- Once a terminal state is reached, it cannot be changed

---

### Row Level Security (RLS)

#### Read access

- Users can read **their own** payment intents
- Admins can read **all** payment intents
- System role can read all rows (webhooks, background jobs)

#### Write access

- Inserts:
  - Allowed for system role only (webhooks / backend)
- Updates:
  - Allowed for system role only
  - Restricted by triggers enforcing immutability and status transitions

---

### Delete behavior

- `DELETE` is not permitted
- Payment intents are append-only records with updates only

---

### Relevant scripts

- [Table definition](./01_app/09_payment_intent.sql)
- [Row level security](./01_app/32_payment_intent_row_level_security.sql)
- [Permissions](./01_app/33_payment_intents_indexes.sql)
- [Indexes](./01_app/34_payment_intents_indexes.sql)
- [Triggers](./01_app/35_payment_intents_triggers.sql)

---

### Notes

- Stripe (or other providers) are the authority on payment outcome
- Database guarantees consistency and auditability
- Application code cannot corrupt or rewrite payment history
- Credits, refunds, and accounting are handled in separate tables

---

## `app.refresh_tokens`

### Purpose

- Stores hashed refresh tokens for authentication
- Enables session continuity and token rotation
- Used exclusively by backend authentication logic
- Never exposed directly to end users

---

### Lifecycle rules

- Tokens are created on login or refresh
- Each token has an expiration (`expires_at`)
- Tokens may be revoked via `revoked_at`
- Token rotation is supported via `replaced_by_token`
- Revoked or expired tokens are permanently invalid

---

### Invariants

- `expires_at` must be after `created_at`
- `revoked_at`, if set, must be after `created_at`
- A token hash is unique
- Plaintext tokens are never stored
- Tokens are immutable except for revocation / rotation metadata

---

### Row Level Security (RLS)

#### Read access

- Allowed for:
  - `app_system`
- End users and app-level admins cannot read refresh tokens

#### Insert access

- Allowed for:
  - `app_system`
- Used during:
  - login
  - refresh token rotation

#### Update access

- Allowed for:
  - `app_system`
- Intended usage:
  - revoke token (`revoked_at`)
  - rotate token (`replaced_by_token`)

#### Delete access

- Not permitted
- Tokens are invalidated via revocation or expiration only

---

### Delete behavior

- Hard deletes are not allowed
- Token invalidation is handled logically

---

### Relevant scripts

- [Table definition](./01_app/10_refresh_tokens.sql)
- [Row level security](./01_app/36_refresh_tokens_row_level_security.sql)
- [Permissions](./01_app/37_refresh_tokens_permissions.sql)
- [Indexes](./01_app/38_refresh_tokens_indexes.sql)
- [Triggers](./01_app/39_refresh_tokens_triggers.sql)

---

### Notes

- All access control is enforced at the database level
- Token rotation is expected on every refresh
- Expired tokens should be ignored by the application
- Optional cleanup can be handled via background jobs

---

## `app.invite_tokens`

### Purpose

- One-time invite links used for user registration
- Generated by admins or system processes
- Token-based authentication mechanism
- Designed for high-volume inserts and short-lived usage

---

### Lifecycle rules

- Tokens are generated in advance (bulk-friendly)
- Tokens expire at `expires_at`
- A token may be used **once**
- Usage is tracked via `used_at`
- Tokens may be hard-deleted after use or expiration

---

### Invariants

- A token cannot be used before creation
- A token cannot be used more than once
- Token hashes are stored, never plaintext
- Expired tokens are always invalid
- Tokens are immutable except for `used_at`

---

### Row Level Security (RLS)

#### Read access

- Allowed for:
  - `app_system`
  - App-level admins

#### Insert access

- Allowed for:
  - `app_system`
  - App-level admins
- Intended for:
  - bulk invite generation
  - automated provisioning

#### Update access

- Allowed for:
  - `app_system`
- Intended use:
  - marking token as used (`used_at`)

#### Delete access

- Allowed for:
  - `app_system`
- Intended for:
  - cleanup of used or expired tokens

---

### Delete behavior

- Hard deletes are allowed
- Tokens have no audit value after use
- Cleanup is expected to be handled via:
  - background jobs
  - scheduled tasks (e.g. `pg_cron`)

---

### Relevant scripts

- [Table definition](./01_app/11_invite_tokens.sql)
- [Row level security](./01_app/38)
- [Permissions](./01_app/41_invite_tokens_permissions.sql)
- [Indexes](./01_app/42_invite_tokens_indexes.sql)
- [Triggers](./01_app/43_invite_tokens_triggers.sql)

---

### Notes

- No foreign keys by design (tokens are ephemeral)
- Tokens should be validated using:
  - expiration
  - unused status
- This table is optimized for write-heavy workloads
- Cleanup strategy is intentionally externalized

---

## `app.session_participation`

### Purpose

- Represents a **user’s registration** to a session
- Handles **business-critical participation state**
- Acts as the **source of truth** for:
  - who registered
  - who cancelled
  - when those actions occurred
- **Financially sensitive**: rows are never hard-deleted

---

### Conceptual model

- A participation row represents a **contractual intent to attend**
- Attendance is tracked separately in `app.session_attendance`
- Participation may exist **without attendance**
- Attendance may **never exist without participation**

---

### Lifecycle rules

- Participation is created when a user registers
- A participation may be cancelled **only before session start**
- Cancellation is **irreversible**
- After session start:
  - participation becomes immutable
- Rows are **never deleted**

---

### Invariants

- A user may register **only once per session**
- A cancelled participation:
  - cannot be modified
  - cannot be attended
- Participation cannot be created after session start
- Cancellation cannot occur after session start
- No role may hard-delete a participation
- Attendance marking is not handled in this table

---

### Row Level Security (RLS)

#### Read access

- Users may read **their own participations**
- Coaches may read participations for **their own sessions**
- Admins may read **all participations**

---

#### Insert access

##### Self registration (users only)

- Allowed only if:
  - `user_id = current_user`
  - `cancelled_at IS NULL`
- Session must not have started
- Admins **do not** register users

---

#### Update access

##### Self cancellation (users)

- Allowed only if:
  - user owns the row
  - participation is active
- Result:
  - `cancelled_at` must transition from `NULL → NOT NULL`
- No other columns may be modified

##### Admin cancellation (exceptional)

- Allowed only to:
  - set `cancelled_at`
- Intended for:
  - operational or support interventions
- Admins may not modify any other fields

---

### Delete behavior

- `DELETE` is **not permitted**
- All lifecycle changes are handled via `UPDATE`
- Historical participation data is preserved permanently

---

### Enforcement notes

- Temporal rules are enforced via **database triggers**
- RLS defines **who** may act
- Triggers define **when** actions are allowed
- Permissions prevent unintended write paths
- Application code **cannot bypass** participation rules
- Financial integrity is preserved at the database layer

---

### Related tables

- `app.sessions`
- `app.users`
- `app.session_attendance`

---

### Relevant scripts

- [Table definition](./01_app/12_session_participation.sql)
- [Row level security](./01_app/44_session_participation_row_level_security.sql)
- [Permissions](./01_app/45_session_participation_permissions.sql)
- [Indexes](./01_app/46_session_participation_indexes.sql)
- [Triggers](./01_app/47_session_participation_triggers.sql)

---

## `app.session_attendance`

### Purpose

- Records **actual attendance** for sessions
- Represents the **final ground truth** of who showed up
- Append-only, business-critical table
- Used for:
  - attendance lists
  - admin exports
  - reporting / compliance

---

### Design principles

- Attendance is **written once**
- No updates, no deletes
- Mistakes are prevented at the UX layer
- Database enforces **temporal correctness**
- Participation (`session_participation`) remains the source of registration truth

---

### Lifecycle rules

- Attendance can only be recorded:
  - **at or after session start**
- Attendance may be recorded:
  - during the session
  - after the session ends
- Attendance cannot be modified once written
- Cancelled participants are **never inserted**
- Non-cancelled participants not present are implicitly treated as absent

---

### Invariants

- One attendance record per `(session_id, user_id)`
- Attendance is immutable after insertion
- Attendance cannot exist before session start
- Attendance does not imply registration — enforced via business logic
- No role may update or delete attendance rows

---

### Row Level Security (RLS)

#### Read access

- **Admins only**
  - Used for:
    - attendance lists
    - exports
    - audits
- Application users do **not** read this table directly

#### Insert access

- **Coach only**
- Conditions:
  - coach must own the session
  - current time must be `>= session.starts_at`
- Scope:
  - insert only
- Updates are intentionally **not allowed**

---

### Write model

- `INSERT` only
- No `UPDATE`
- No `DELETE`
- All corrections must happen before submission

---

### Enforcement notes

- RLS controls **who** can write or read
- Triggers enforce **when** attendance can be written
- Unique constraint prevents double attendance
- Application layer validates:
  - participant exists
  - participant was not cancelled

---

### Indexing strategy

- `UNIQUE (session_id, user_id)`
  - ensures integrity
  - provides a composite unique index
- Additional index:
  - `session_id` for fast attendance list queries

---

### Relevant scripts

- [Table definition](./01_app/13_session_attendance.sql)
- [Row level security](./01_app/48_session_attendance_row_level_security.sql)
- [Permissions](./01_app/49_session_attendance_permissions.sql)
- [Indexes](./01_app/50_session_attendance_indexes.sql)
- [Triggers](./01_app/51_session_attendance_triggers.sql)

---

## `app.credit_ledger`

### Purpose

- Immutable **financial ledger** for user credits
- Represents the **single source of truth** for credit balance
- Records *every* credit movement:
  - payments
  - refunds
  - session usage
  - admin adjustments
- Business-critical, compliance-grade table

---

### Design principles

- **Append-only**
- No updates, no deletes
- Balance is stored **explicitly** and validated at insert time
- Historical integrity is enforced **at the database level**
- Ledger correctness does **not** rely on application code

---

### Ledger semantics

- `amount_cents`
  - positive → credit added
  - negative → credit spent
- `balance_after_cents`
  - absolute balance **after** applying `amount_cents`
  - must never be negative
- `cause`
  - describes *why* the ledger entry exists
- `payment_intent_id`
  - required for payment-related causes
  - forbidden otherwise

---

### Lifecycle rules

- Ledger entries are created **once**
- Entries are never modified
- Entries are never deleted
- Ledger grows monotonically over time per user
- Balance must be consistent with previous entry

---

### Invariants

- Ledger is append-only
- `amount_cents <> 0`
- `balance_after_cents >= 0`
- Balances must be **sequential**
- Entries must be **chronological per user**
- `payment_intent_id` rules:
  - required for `payment`, `refund`
  - forbidden for all other causes

---

### Row Level Security (RLS)

#### Read access

- Users can read **their own ledger**
- Admins can read **all ledger entries**
- System role can read for internal processing

#### Insert access

- **System only**
- All inserts are validated via triggers

#### Update / Delete access

- Not allowed
- Explicitly blocked by triggers

---

### Write model

- `INSERT` only
- No `UPDATE`
- No `DELETE`
- Ledger corrections require **new compensating entries**

---

### Enforcement notes

- RLS controls **who** may access data
- Triggers enforce:
  - append-only behavior
  - balance correctness
  - chronological ordering
  - cause ↔ payment intent consistency
- Application code cannot:
  - rewrite history
  - skip balances
  - reorder entries

---

### Indexing strategy

- `PRIMARY KEY (id)`
- Index on:
  - `(user_id)`
  - `(user_id, created_at DESC)`
  - `(payment_intent_id)` where not null

---

### Relevant scripts

- [Table definition](./01_app/14_credit_ledger.sql)
- [Row level security](./01_app/52_credit_ledger_row_level_security.sql)
- [Permissions](./01_app/53_credit_ledger_permissions.sql)
- [Indexes](./01_app/54_credit_ledger_indexes.sql)
- [Triggers](./01_app/55_credit_ledger_triggers.sql)

---

## `app.payment`

### Purpose

- Records **finalized, provider-confirmed payments**
- Represents **real money movements** confirmed by external providers
- Used for:
  - billing records
  - financial reconciliation
  - audits and dispute resolution
- Source of truth for **successful payments only**

---

### Design principles

- **Immutable**
- One row per successful payment
- Insert-only
- No updates, no deletes
- Idempotent by provider identifiers
- Database-enforced correctness

---

### Payment semantics

- `user_id`
  - user who owns and initiated the payment
- `session_id`
  - session the payment is associated with
- `provider`
  - external payment processor (e.g. `stripe`)
- `provider_payment_id`
  - provider-side unique identifier
  - enforces idempotency
- `amount_cents`
  - strictly positive integer
- `currency`
  - ISO 4217 uppercase 3-letter code

---

### Lifecycle rules

- Payments are created **once**
- Payments are never modified
- Payments are never deleted
- Failed or pending payments **do not belong here**
- Corrections require:
  - refunds
  - compensating entries elsewhere (e.g. credit ledger)

---

### Invariants

- Table is **append-only**
- `amount_cents > 0`
- `currency` must match `^[A-Z]{3}$`
- `(provider, provider_payment_id)` is unique
- Each row represents a **provider-confirmed payment**

---

### Row Level Security (RLS)

#### Read access

- Users can read **their own payments**
- App-level admins (via roles table) can read **all payments**
- System role can read for internal processing

#### Insert access

- **System only**
- Inserted after provider confirmation

#### Update / Delete access

- Not allowed
- Explicitly blocked by triggers

---

### Write model

- `INSERT` only
- No `UPDATE`
- No `DELETE`
- Payment state transitions are handled **outside** this table

---

### Enforcement notes

- RLS controls **who** can see which payments
- Permissions restrict **who** can write
- Triggers enforce:
  - immutability
- Application code cannot:
  - alter payment history
  - forge provider confirmations
  - mutate monetary records

---

### Indexing strategy

- `PRIMARY KEY (id)`
- Unique index on:
  - `(provider, provider_payment_id)`
- Indexes on:
  - `(user_id)`
  - `(session_id)`
  - `(created_at)`

---

### Relevant scripts

- [Table definition](./01_app/15_payment.sql)
- [Row level security](./01_app/56_payment_row_level_security.sql)
- [Permissions](./01_app/57_payment_permissions.sql)
- [Indexes](./01_app/58_payment_indexes.sql)
- [Triggers](./01_app/59_payment_triggers.sql)

---

## `audit.events`

### Purpose

- Immutable **audit log** for security- and compliance-critical events
- Acts as the **last line of defense** for forensic analysis
- Records **who did what, when, and to what**
- Not used by application business logic
- Consulted **only during incidents, disputes, or investigations**

---

### Design principles

- **Append-only**
- Write-once, read-rarely
- Zero trust in application correctness
- Database-enforced integrity
- Optimized for **truth**, not convenience

---

### Event semantics

- `actor_type`
  - origin of the event
  - examples: `user`, `system`, `stripe`
- `actor_id`
  - UUID of the acting entity
  - nullable for system / external actors
- `event_type`
  - semantic identifier of the action
  - examples: `SESSION_CREATED`, `USER_DISABLED`, `PAYMENT_CONFIRMED`
- `target_id`
  - entity affected by the event
  - nullable when not applicable
- `metadata`
  - structured, schemaless context
  - never updated after insertion

---

### Lifecycle rules

- Events are written **once**
- Events are never modified
- Events are never deleted
- History is **permanent**
- Corrections require **new events**, never edits

---

### Invariants

- Table is **INSERT-only**
- No `UPDATE`
- No `DELETE`
- `occurred_at` reflects creation time
- Rows are immutable after insertion

---

### Row Level Security (RLS)

- **Not enabled**
- Table is not queried by application users
- Access is controlled strictly via:
  - database roles
  - schema ownership
  - GRANT / REVOKE

Rationale:

- Audit data must remain readable even during RLS misconfiguration
- Visibility is intentionally centralized and restricted

---

### Write model

- `INSERT` only
- Writes performed by:
  - `app_system`
  - trusted background jobs
- No application-level reads

---

### Enforcement notes

- Triggers enforce:
  - append-only behavior
  - immutability of all rows
- Permissions enforce:
  - no UPDATE / DELETE / TRUNCATE
  - no CREATE in audit schema
- Even database admins cannot mutate data accidentally

---

### Indexing strategy

- No additional indexes by default
- Table is expected to be:
  - write-heavy
  - read-rarely
- Indexes may be added **only** if incident response requires it

---

### Relevant scripts

- [Table definition](./02_audit/01_events.sql)
- [Permissions & schema lockdown](./02_audit/02_audit_permissions.sql)
- [Immutability triggers](./02_audit/03_events_triggers.sql)

---
