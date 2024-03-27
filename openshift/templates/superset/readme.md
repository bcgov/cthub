

https://artifacthub.io/packages/helm/superset/superset

helm repo add superset http://apache.github.io/superset/

helm upgrade --install --set 
cthub-superset-dev superset/superset --version 0.10.14


supersetNode.connections.redis_host=cthub-redis-dev-headless
supersetNode.connections.redis_password=xxx
supersetNode.connections.db_host=cthub-crunchy-dev-pgbouncer
supersetNode.connections.db_user=xxx
supersetNode.connections.db_pass=xxx


supersetNode.connections.redis_password=xxxxx\\


create supersetuser in database

update patroni secret to ass superset_username and superset_password

create superset user and superset database in crunchy



