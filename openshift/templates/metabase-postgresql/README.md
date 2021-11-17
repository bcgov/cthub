## Files included
* Dockerfile build metabase 
* metabase-bc.yaml build metabase image on Openshift
* metabase-dc.yaml deploy metabase image on Openshift
* metabase-secret.yaml includes metabase credentials, it is referenced by metabase-dc.yaml

## Create metabase database on existing patroni cluster
CREATE USER [username] WITH PASSWORD '[password]'
CREATE DATABASE metabase OWNER [username]
