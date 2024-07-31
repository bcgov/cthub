### Files included

- minio-bc.yaml minio build config
- minio-dc.yaml minio deployment config
- secret-template.yaml the secret template

### build minio

oc import-image rhel7/rhel:7.9-508 --from=registry.redhat.io/rhel7/rhel:7.9-508 --confirm
oc process -f ./minio-bc.yaml GIT_REF= | oc create -f - -n 30b186-tools
oc tag minio:latest minio:20211020 -n 30b186-tools

### One minio instance serve all PRs on Dev

oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=dev SUFFIX=-dev \
| oc create -f - -n 30b186-dev

#### Test and Prod Minio setup

oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=test SUFFIX=-test \
| oc create -f - -n 30b186-test

oc process -f ./minio-dc.yaml \
NAME=cthub ENV_NAME=prod SUFFIX=-prod \
| oc create -f - -n 30b186-prod
