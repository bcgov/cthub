## Files included
* Dockerfile build metabase 
* metabase-bc.yaml build metabase image on Openshift
* metabase-dc.yaml deploy metabase image on Openshift

## Metabase to TFRS and ZEVA database access
The network policy allow-patroni-accepts-cthub-metabase-test in both TFRS and ZEVA open the access from the Metabase in CTHUB.

## Create read only user metabaseuser in both TFRS and ZEVA for Metabase connection from CTHUB
```//login as postgres user
CREATE USER metabaseuser WITH PASSWORD 'xxxxxx';
GRANT CONNECT ON DATABASE zeva TO metabaseuser;
//login to zeva database user as database owner
GRANT USAGE ON SCHEMA public TO metabaseuser;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabaseuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabaseuser;
// verify permissions are granted.  select * from information_schema.role_table_grants where grantee='metabaseuser';
```
Notes: replace zeva to be tfrs when ron on TFRS project
