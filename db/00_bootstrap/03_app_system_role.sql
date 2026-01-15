-- Application system user (webhooks, cron, admin actions)
CREATE ROLE app_system
  LOGIN
  PASSWORD 'CHANGE_ME_APP'
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  INHERIT;