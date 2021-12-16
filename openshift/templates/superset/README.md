oc process -f ./superset-dc.yaml ENV_NAME=test SUFFIX=-test \
CPU_REQUEST=300m CPU_LIMIT=500m MEMORY_REQUEST=500M MEMORY_LIMIT=2G REPLICAS=1 | \
oc apply -f - -n 30b186-test


