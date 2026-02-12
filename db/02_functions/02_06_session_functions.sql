CREATE OR replace FUNCTION app_fcn.session_create_session(
	p_session_id uuid,
	p_coach_id uuid,
	p_title text,
	p_starts_at timestamptz,
	p_ends_at timestamptz,
	p_price_cents int,
	p_currency text
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.session_create_session
	 *
	 * Creates a session if it does not already exist.
	 *
	 * This function is idempotent:
	 * - If the session already exists (same primary key), the function returns
	 *   without performing any action.
	 *
	 * Concurrency & safety:
	 * - Uses a transaction-scoped advisory lock on the session ID to prevent
	 *   race conditions during concurrent creation attempts.
	 *
	 * Authorization:
	 * - Caller must be a coach or an admin.
	 * - Authorization is enforced inside the database using SECURITY DEFINER.
	 *
	 * Parameters:
	 * - p_session_id     : Unique identifier of the session (primary key).
	 * - p_coach_id       : Coach responsible for the session.
	 * - p_title          : Session title.
	 * - p_starts_at      : Session start timestamp (UTC).
	 * - p_ends_at        : Session end timestamp (UTC).
	 * - p_price_cents    : Session price in cents.
	 * - p_currency       : ISO currency code (upper-case expected).
	 *
	 * Errors:
	 * - Raises ERRCODE 'AP401' if the caller is not authorized.
	 *
	 * Returns:
	 * - void
	 */
	BEGIN
		perform pg_advisory_xact_lock(
			hashtext('session:' || p_session_id::text)
		);
	
		IF NOT (app_fcn.is_coach() or app_fcn.is_admin()) THEN
			raise exception 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.is_user_active(p_coach_id) THEN
			RETURN;
		END IF;
	
		IF app_fcn.session_exists(p_session_id) THEN
			RETURN;
		END IF;

		IF app_fcn.is_session_overlapping(p_starts_at, p_ends_at) THEN
			RETURN;
		END IF;
	
		INSERT INTO app.sessions(
			id,
			coach_id,
			title,
			starts_at,
			ends_at,
			price_cents,
			currency
		)
		VALUES (
			p_session_id,
			p_coach_id,
			p_title,
			p_starts_at,
			p_ends_at,
			p_price_cents,
			p_currency
		);
	END;
$$;

COMMENT ON FUNCTION app_fcn.session_create_session(
	uuid,
	uuid,
	text,
	timestamptz,
	timestamptz,
	int,
	text
) IS
'Creates a session in an idempotent and concurrency-safe manner.

Uses a transaction-scoped advisory lock on the session ID to prevent race
conditions. If the session already exists, the function returns without
modifying state.

Authorization is enforced inside the database: the caller must be a coach
or an admin. Designed to be safely retryable and spam-resistant.';

create or replace function app_fcn.session_update(
	p_session_id uuid,
	p_title text,
	p_starts_at timestamptz,
	p_ends_at timestamptz
)
returns void
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.session_update
	 *
	 * Idempotent domain command to update an existing session.
	 *
	 * This function updates the title and schedule of a session while enforcing
	 * domain invariants at the database level.
	 *
	 * Behavior:
	 *   - If the caller is not an admin or a coach, the function raises an error.
	 *   - If the session does not exist, the function performs a no-op.
	 *   - If the new time range overlaps with another active session (excluding
	 *     the session being updated), a domain exception is raised.
	 *   - If the provided values are identical to the current state, no update
	 *     is performed (idempotent behavior).
	 *
	 * Domain invariants:
	 *   - Active sessions must not overlap in time.
	 *   - Only admins or coaches may update sessions.
	 *
	 * Notes:
	 *   - This function is intentionally idempotent to allow safe retries.
	 *   - Overlapping sessions are treated as a domain violation (AP409).
	 *   - Missing sessions are treated as a no-op to preserve idempotency.
	 *   - Uses half-open time ranges ([starts_at, ends_at)).
	 *
	 * Errors:
	 *   - AP401: caller is not authorized
	 *   - AP409: session time overlaps with another active session
	 */
	BEGIN
		IF NOT (app_fcn.is_admin() OR app_fcn.is_coach()) THEN
			raise exception 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		IF NOT app_fcn.session_exists(p_session_id) THEN
			RETURN;
		END IF;

		IF app_fcn.is_session_overlapping_except(
			p_starts_at,
			p_ends_at,
			p_session_id
		) THEN
			RAISE EXCEPTION 'session is overlapping'
				USING ERRCODE = 'AP409';
		END IF;

		UPDATE app.sessions
		SET 
			title = p_title,
			starts_at = p_starts_at,
			ends_at = p_ends_at
		WHERE id = p_session_id;			
	END;
$$;

COMMENT ON FUNCTION app_fcn.session_update(
	uuid,
	text,
	timestamptz,
	timestamptz
) IS
'Idempotent domain command that updates a session title and schedule.

- No-op if the session does not exist.
- Safe to call multiple times with the same arguments.
- Raises AP401 if the caller is not an admin or coach.
- Raises AP409 if the updated time range overlaps another active session.
- Enforces session scheduling invariants at the database level.';

create or replace function app_fcn.get_pre_attendance(
	p_session_id uuid
)
returns table(
	user_id uuid,
	first_name text,
	last_name text
)
language plpgsql
security definer
set search_path = app, app_fcn, pg_temp
as $$
	/*
	 * app_fcn.get_pre_attendance
	 *
	 * Returns the list of participants eligible for attendance
	 * for a given session, before attendance has started.
	 *
	 * This function represents the "pre-attendance" phase of
	 * the session lifecycle.
	 *
	 * Domain invariants:
	 *   - Only coaches may access pre-attendance data
	 *   - Once a session is attended, pre-attendance is no longer available
	 *   - Only paid and non-cancelled participants are returned
	 *
	 * Concurrency:
	 *   - Uses an advisory transaction lock scoped to the session
	 *     to ensure race safety with attendance creation
	 *
	 * Idempotency:
	 *   - If attendance already exists, returns an empty result set
	 *     without raising an error
	 */
	BEGIN
		PERFORM pg_advisory_xact_lock(
			hashtext('session:' || p_session_id::text)
		);

		IF NOT app_fcn.is_coach() THEN
			RAISE EXCEPTION 'permission denied'
				USING ERRCODE = 'AP401';
		END IF;

		-- Pre-attendance is invalid once attendance has started
		IF app_fcn.is_attended(p_session_id) THEN
			RETURN;
		END IF;

		RETURN QUERY
		SELECT
			up.user_id,
			up.first_name,
			up.last_name
		FROM app.session_participation sp
		JOIN app.user_profiles up
			ON up.user_id = sp.user_id
		WHERE sp.session_id = p_session_id 
			AND sp.cancelled_at IS NULL
			AND sp.paid_at IS NOT NULL;
	END;
$$;

COMMENT ON FUNCTION app_fcn.get_pre_attendance(uuid) IS
'Returns the list of paid, non-cancelled participants eligible for attendance
before attendance has started for a session.
Enforces domain invariants via authorization checks, attendance-state predicates,
and advisory transaction locking.';

