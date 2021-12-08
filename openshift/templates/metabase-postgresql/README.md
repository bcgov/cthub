## Files included
* Dockerfile build metabase 
* metabase-bc.yaml build metabase image on Openshift
* metabase-dc.yaml deploy metabase image on Openshift

## Metabase to TFRS and ZEVA database access
The network policy allow-patroni-accepts-cthub-metabase-test in both TFRS and ZEVA open the access from the Metabase in CTHUB.

## Create read only user metabaseuser in both TFRS and ZEVA for Metabase connection from CTHUB
```//login zeva database as postgres user, psql zeva
CREATE USER metabaseuser WITH PASSWORD 'xxxxxx';
GRANT CONNECT ON DATABASE zeva TO metabaseuser;
GRANT USAGE ON SCHEMA public TO metabaseuser;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabaseuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabaseuser;
// verify permissions are granted.  select * from information_schema.role_table_grants where grantee='metabaseuser';
```
Notes: replace zeva to be tfrs when ron on TFRS project
Login to metabase pod and test the connection to tfrs and zeva database
```
curl patroni-master-[env].e52f12-[env].svc.cluster.local:5432
curl patroni-master-[env].0ab226-[env].svc.cluster.local:5432
```