-- Restrict access explicitly to prevent accidental exposure
REVOKE ALL ON app.v_coach_public FROM PUBLIC;

-- Allow read-only access for API user role
GRANT SELECT ON app.v_coach_public TO app_user;

-- Ensure view executes with table-owner privileges
ALTER VIEW app.v_coach_public OWNER TO app_admin;