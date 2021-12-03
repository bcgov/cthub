## Build and deploy Patroni 2.1.1 on top of Postgresql 12.4

### Files included
* The files included are from https://github.com/bcgov/patroni-postgres-container.git
* The post_init.sh is changed to create extensions and metabase db and user
* The deploy.yaml is changed to provide metabase credentials

### How to create patroni cluster
* Use build.yaml to build patroni image and store it under tools project
* Use secret-template.yaml to create template.paroni-patroni
* Use deploy.yaml to deploy to test and prod environment
* For dev environment, patroni is part of pipeline
