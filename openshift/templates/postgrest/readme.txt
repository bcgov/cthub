== Postgrest research on test env
create role web_anon nologin;
  # GRANT CONNECT ON DATABASE cthub TO web_anon;
GRANT USAGE ON SCHEMA public TO web_anon;
GRANT SELECT ON public.vehicle TO web_anon;
  # ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO web_anon;
create role authenticator noinherit login password 'xxxxx';
GRANT web_anon to authenticator;

select * from information_schema.role_table_grants where grantee='web_anon';

openssl rand -hex 64
