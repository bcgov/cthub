### Files included

* minio-bc.yaml minio build config
* minio-dc.yaml minio deployment config
* minio-secret.yaml create template.minio-secret, it is NOT being used as minio creation is not part of pipeline anymore

### build minio

oc import-image rhel7/rhel:7.9-508 --from=registry.redhat.io/rhel7/rhel:7.9-508 --confirm
oc process -f ./minio-bc.yaml | oc create -f - -n b03186-tools
oc tag minio:latest minio:20211020

### One minio instance serve all PRs on Dev

oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=dev SUFFIX=-dev OCP_NAME=apps.silver.devops \
| oc create -f - -n 30b186-dev

#### Test and Prod Minio setup

oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=test SUFFIX=-test OCP_NAME=apps.silver.devops \
| oc create -f - -n 30b186-test


oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=prod SUFFIX=-prod OCP_NAME=apps.silver.devops \
| oc create -f - -n 30b186-prod