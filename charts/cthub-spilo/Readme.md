## Before running Helm
* Create secret cthub-patroni-admin
    * Create the secret by using cthub/openshift/templates/spilo/cthub-patroni-admin.yaml, the three passwords are generated randomly

* Create secret cthub-patroni-app
    * Create the secret by using cthub/openshift-v4/templates/spilo/cthub-patroni-app.yaml, the three password fields must be in sync with the existing secret patroni-dev
    * It contains: app-db-name, app-db-password, app-db-username, metabaseuser-name, metabaseuser-password
    * The replication- and superuser- are not needed
    * If this secret is aleady existed, please verify the password fields

* Create Object Storage secret for database continuous backup, cthub-object-storage
    * Create the secret by using cthub/openshift-v4/templates/object-storage/object-storage-secret.yaml
    * The secret should have been created, verify it by using CyberDuck

* Create secret cthub-db-backup-s3
    * It includes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_ENDPOINT
    * The values are in sync with secret cthub-object-storage

* Verify values-dev.yaml. Create the bucket on object storage if needed

* Add new KNPs templates/knp/knp-env-pr-new-cthub-spilo.yaml
    * oc process -f ./knp-env-pr-new-cthub-spilo.yaml ENVIRONMENT=test | oc apply -f - -n 30b186-dev    

## Heml command
helm install -n 30b186-dev -f ./values-dev.yaml cthub-spilo .
helm uninstall -n 30b186-dev cthub-spilo

## Migrate Postgresql 10 on Patroni to 14 on Spilo container

### Bring down the cthub application and route the frontend to maintenance mode

### Run a final backup on backup container

### Create cthub database user and database
* Login to the cthub-spilo leader pod
* If the username contains upper case letters, should be double quoted
    * create user for cthub database, the username should be the same on v10 otherwise the restore may encounter issue
        * create user [username] with password '[password]'
        * The password can be found in secret cthub-patroni-app
    * create cthub database
        * create database cthub owner [username] ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8'
### Reset postgresql logging
* login cthub-spilo leader pod, run the following psql to only keep 24 hours log files, otherwise they take too much space
    ALTER SYSTEM SET log_filename='postgresql-%H.log';
    ALTER SYSTEM SET log_connections='off';
    ALTER SYSTEM SET log_disconnections='off';
    ALTER SYSTEM SET log_checkpoints='off';
    select pg_reload_conf();
### Create metabase user
* login cthub-spilo leader pod
    CREATE USER metabaseuser WITH PASSWORD 'xxxxxx';
    GRANT CONNECT ON DATABASE cthub TO metabaseuser;
    GRANT USAGE ON SCHEMA public TO metabaseuser;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabaseuser;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabaseuser;
    verify permissions are granted:  select * from information_schema.role_table_grants where grantee='metabaseuser';

## Backup the existing v10 database and restore to v14 cluster
* Make sure the application is stopped
* Login to patroni-dev leader pod
    * make an empty dir /home/postgres/migration and cd into it
    * backup cthub database: pg_dump cthub > cthub.sql
* Restore cthub database
    * psql cthub < ./cthub.sql >> ./restore.log 2>&1
    * verify the restore.log when complete

* Point the applications to v14 cluster, update the enviuronment variables for
    * backend: DATABASE_SERVICE_NAME, POSTGRESQL_SERVICE_HOST
    * celery: DATABASE_SERVICE_NAME
    * scan-handler: DATABASE_SERVICE_NAME
* Bring down the v10 cluster
* Bring down the maintenance page
* Bring up the cthub appliation
* Update patroni backup to only backup minio data
* Update metabase connection from CTHUB
* Update dbServiceName to be cthub-spilo in .pipeline/lib/config.js

## Notes for uninstalling cthub-spilo when needed
* After the helm uninstall command, remember to remove the followings:
    * The two configmaps: cthub-spilo-config, cthub-spilo-leader
    * The PVCs storage-volume-cthub-spilo-*
    * The backup bucket in object storage
