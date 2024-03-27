# Redis

## Source

* https://artifacthub.io/packages/helm/bitnami/redis

* https://github.com/bitnami/charts/tree/main/bitnami/redis

### Install and Version

helm repo add bitnami https://charts.bitnami.com/bitnami  

helm -n 30b186-dev upgrade --install -f ./cthub-dev-values.yaml cthub-redis-dev bitnami/redis --version 18.2.0  
helm -n 30b186-test upgrade --install -f ./cthub-test-values.yaml cthub-redis-test bitnami/redis --version 18.2.0  

helm -n 30b186-dev uninstall cthub-redis-dev

cthub-redis-dev-replicas-1
