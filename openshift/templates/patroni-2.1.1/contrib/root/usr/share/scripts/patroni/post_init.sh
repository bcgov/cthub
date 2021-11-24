#!/usr/bin/env bash
set -Eeu

if [[ (! -z "$APP_USER") &&  (! -z "$APP_PASSWORD") && (! -z "$APP_DATABASE")]]; then
  echo "Creating user ${APP_USER}"
  psql "$1" -w -c "create user \"${APP_USER}\" WITH LOGIN ENCRYPTED PASSWORD '${APP_PASSWORD}'"
  echo "Creating user ${METABASE_USER}"
  psql "$1" -w -c "create user \"${METABASE_USER}\" WITH LOGIN ENCRYPTED PASSWORD '${METABASE_PASSWORD}'"

  echo "Creating database ${APP_DATABASE}"
  psql "$1" -w -c "CREATE DATABASE \"${APP_DATABASE}\" OWNER \"${APP_USER}\" ENCODING '${APP_DB_ENCODING:-UTF8}' LC_COLLATE = '${APP_DB_LC_COLLATE:-en_US.UTF-8}' LC_CTYPE = '${APP_DB_LC_CTYPE:-en_US.UTF-8}'"
  echo "Creating database ${METABASE_DATABASE}"
  psql "$1" -w -c "CREATE DATABASE \"${METABASE_DATABASE}\" OWNER \"${METABASE_USER}\" ENCODING '${METABASE_DB_ENCODING:-UTF8}' LC_COLLATE = '${METABASE_DB_LC_COLLATE:-en_US.UTF-8}' LC_CTYPE = '${METABASE_DB_LC_CTYPE:-en_US.UTF-8}'"
  
  echo "Creating extension hstore for ${APP_DATABASE}" 
  psql -U postgres -q -d "${APP_DATABASE}" -c 'create extension if not exists hstore'
  echo "Creating extension citext for ${METABASE_DATABASE}" 
  psql -U postgres -q -d "${METABASE_DATABASE}" -c 'create extension if not exists citext'

else
  echo "Skipping user creation"
  echo "Skipping database creation"
fi
