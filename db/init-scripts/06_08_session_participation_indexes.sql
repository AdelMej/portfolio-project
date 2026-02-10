\c app

-- ------------------------------------------------------------------
-- Indexes: app.session_participation
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Active participant lookups by user
--
-- Used by:
-- - RLS in app.user_profiles (participant ↔ participant, participant → coach)
-- - Fast joins for session queries
--
-- Partial index for active (non-cancelled) participations
-- ---------------------------------------------------------------
CREATE INDEX idx_sp_active_user_id
ON app.session_participation(user_id)
WHERE cancelled_at IS NULL;

COMMENT ON INDEX app.idx_sp_active_user_id IS
'Optimizes lookups of active participants by user_id, used in RLS and joins.';

-- ---------------------------------------------------------------
-- Active participant lookups by session
--
-- Used by:
-- - RLS in app.user_profiles (coach → participant, participant ↔ participant)
-- - Fast joins for session queries
--
-- Partial index for active (non-cancelled) participations
-- ---------------------------------------------------------------
CREATE INDEX idx_sp_active_session_id
ON app.session_participation(session_id)
WHERE cancelled_at IS NULL;

COMMENT ON INDEX app.idx_sp_active_session_id IS
'Optimizes lookups of active participants by session_id, used in RLS and joins.';

-- ---------------------------------------------------------------
-- Fast general lookup on user_id
--
-- Used by:
-- - Any non-RLS queries filtering by user_id
-- ---------------------------------------------------------------
CREATE INDEX idx_sp_user_id
ON app.session_participation(user_id);

COMMENT ON INDEX app.idx_sp_user_id IS
'Accelerates queries filtering or joining on user_id.';

-- ---------------------------------------------------------------
-- Fast general lookup on session_id
--
-- Used by:
-- - Any non-RLS queries filtering by session_id
-- ---------------------------------------------------------------
CREATE INDEX idx_sp_session_id
ON app.session_participation(session_id);

COMMENT ON INDEX app.idx_sp_session_id IS
'Accelerates queries filtering or joining on session_id.';

-- ---------------------------------------------------------------
-- Prevent double registration enforcement
--
-- Used by:
-- - Queries validating uniqueness before inserts (extra safety)
-- ---------------------------------------------------------------
CREATE UNIQUE INDEX idx_sp_user_session_unique
ON app.session_participation(session_id, user_id);

COMMENT ON INDEX app.idx_sp_user_session_unique IS
'Ensures a user cannot register twice for the same session. Supports fast validation and join operations.';

-- ---------------------------------------------------------------
-- Time-based lookups for analytics
--
-- Used by:
-- - Session activity dashboards
-- - Attendance reporting
-- ---------------------------------------------------------------
CREATE INDEX idx_sp_registered_at
ON app.session_participation(registered_at);

COMMENT ON INDEX app.idx_sp_registered_at IS
'Speeds up queries filtering participations by registration date for analytics and reporting.';
