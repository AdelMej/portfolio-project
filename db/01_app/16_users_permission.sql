-- Users table permissions
REVOKE ALL ON TABLE app.users FROM PUBLIC;
REVOKE ALL ON TABLE app.users FROM app_user;
REVOKE ALL ON TABLE app.users FROM app_system;

-- app_user: can read users and update self (RLS will handle scope)
GRANT SELECT, UPDATE ON TABLE app.users TO app_user;

-- app_system: needs to read users + create them (signup, sync, etc.)
GRANT SELECT, INSERT ON TABLE app.users TO app_system;