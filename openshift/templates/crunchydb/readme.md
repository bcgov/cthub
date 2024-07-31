# Migrate to CrunchyDB

## Create CrunchyDB Cluster

Create Cluster

## Migrate metabase database to CrunchyDB

### Create metabase user under psql prompt

create user **\*\*\*\*** password '**\*\*\*\***';  
create database metabase owner metabaseuser ENCODING 'utf8' LC_COLLATE = 'en_US.utf-8' LC_CTYPE = 'en_US.utf-8';  
CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;  
CREATE EXTENSION IF NOT EXISTS set_user WITH SCHEMA public;

### Dump and restore metabase data

pg_dump -f matabase-data.sql -n public -d metabase  
psql metabase < ./matabase-data.sql >> ./metabase-restore.log 2>&1

## Migrate cthub database to CrunchyDB

create user **\*\*\*\*** password '**\*\*\*\***';  
create database cthub owner cthubpqaitvng ENCODING 'utf8' LC_COLLATE = 'en_US.utf-8' LC_CTYPE = 'en_US.utf-8';  
CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;  
CREATE EXTENSION IF NOT EXISTS set_user WITH SCHEMA public;

### Dump and restore cthub data

pg_dump -f cthub-data.sql -n public -d cthub  
psql cthub < ./cthub-data.sql >> ./cthub-restore.log 2>&1  

