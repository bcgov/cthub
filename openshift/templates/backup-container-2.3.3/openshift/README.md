### Files included

- backup-build.yaml build backup container image
- backup-config.yaml create backup-conf configmap
- backup-deploy.yaml deploy backup container

## Setup Backup container,use Test as example

1. Build patroni-backup image
   oc -n 30b186-tools process -f ./backup/backup-build.yaml \
   -p NAME=patroni-backup GIT_REPO_URL=https://github.com/BCDevOps/backup-container.git GIT_REF=2.3.3 OUTPUT_IMAGE_TAG=2.3.3 \
   | oc -n 30b186-tools apply -f -

2. Create the configmap in env project

3. add to ./config/backup.conf, 9pm run backup, 10pm run verification
   postgres=patroni-master-test:5432/cthub
   postgres=patroni-master-test-metabase:5432/metabase
   0 1 \* \* _ default ./backup.sh -s
   0 7 _ \* _ default ./backup.sh -s
   0 13 _ \* _ default ./backup.sh -s
   0 19 _ \* _ default ./backup.sh -s
   0 22 _ \* \* default ./backup.sh -s -v all

4. create deployment config for backup container
   4.1 for test
   oc -n 30b186-test process -f ./backup-deploy.yaml \
    -p NAME=patroni-backup \
    -p ENV_NAME_UPPERCASE=TEST \
    -p ENV_NAME_LOWERCASE=test \
    -p BACKUP_STRATEGY=rolling \
    -p BACKUP_DIR=/backups/patroni-backup/ \
    -p DAILY_BACKUPS=28 \
    -p WEEKLY_BACKUPS=16 \
    -p MONTHLY_BACKUPS=4 \
    -p CONFIG_MAP_NAME=backup-conf \
    -p CONFIG_MOUNT_PATH=/ \
    -p BACKUP_VOLUME_NAME=backup-test \
    -p VERIFICATION_VOLUME_NAME=backup-verification-test \
    -p VERIFICATION_VOLUME_MOUNT_PATH=/var/lib/pgsql/data \
    -p CPU_REQUEST=35m \
    -p CPU_LIMIT=70m \
    -p MEMORY_REQUEST=50Mi \
    -p MEMORY_LIMIT=100Mi \
    | oc create -f - -n 30b186-test
