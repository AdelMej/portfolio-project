/*
 * app.v_coach_public
 * ------------------
 * Public read-only view exposing basic profile information
 * for users with the "coach" role.
 *
 * This view is intended for public API consumption.
 * It deliberately exposes only non-sensitive fields and
 * prevents direct access to underlying tables.
 *
 * Access model:
 * - SELECT granted to app_user
 * - No write access
 * - Underlying tables remain protected
 */
CREATE OR REPLACE VIEW app.v_coach_public AS
SELECT
    u.user_id,
    u.first_name,
    u.last_name
FROM app.user_profiles u
JOIN app.user_roles ur ON ur.user_id = u.user_id
JOIN app.roles r ON r.id = ur.role_id
WHERE r.role_name = 'coach';

COMMENT ON VIEW app.v_coach_public IS
'Public read-only view exposing basic profile information for users with the coach role. Used by the API to safely list coaches without granting access to underlying tables.';