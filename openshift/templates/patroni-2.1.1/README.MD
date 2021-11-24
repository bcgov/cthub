## Build and deploy Patroni 2.1.1 on top of Postgresql 12.4

### Files included
* The files included are from https://github.com/bcgov/patroni-postgres-container.git
* Use command "oc prcess -f ./secret-template.yaml | oc create -f - -n [env-project]" to create secrete template template.paroni-patroni
* Use pipeline to build patroni image and deploy on environment projects


