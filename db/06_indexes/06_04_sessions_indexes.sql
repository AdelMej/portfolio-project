-- ------------------------------------------------------------------
-- Indexes: app.sessions
-- ------------------------------------------------------------------

-- ---------------------------------------------------------------
-- Coach lookups
--
-- Used by:
-- - coach dashboards
-- - listing sessions owned by a coach
-- ---------------------------------------------------------------

CREATE INDEX idx_sessions_coach_id
ON app.sessions (coach_id);

COMMENT ON INDEX app.idx_sessions_coach_id IS
'Optimizes lookup of sessions by coach. Used for coach-owned session listings.';

-- ---------------------------------------------------------------
-- Time-based browsing
--
-- Used by:
-- - public session browsing
-- - chronological listings
-- - calendar views
-- ---------------------------------------------------------------

CREATE INDEX idx_sessions_starts_at
ON app.sessions (starts_at);

COMMENT ON INDEX app.idx_sessions_starts_at IS
'Supports time-based session browsing and ordering by start time.';

-- ---------------------------------------------------------------
-- Coach dashboard optimization
--
-- Used by:
-- - coach dashboards
-- - upcoming sessions per coach
--
-- Composite index avoids bitmap scans
-- ---------------------------------------------------------------

CREATE INDEX idx_sessions_coach_starts_at
ON app.sessions (coach_id, starts_at);

COMMENT ON INDEX app.idx_sessions_coach_starts_at IS
'Optimizes coach dashboard queries combining coach_id and start time.';
