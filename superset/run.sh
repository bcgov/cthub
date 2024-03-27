#!/usr/bin/env bash
/app/docker/docker-init.sh &

/app/docker/docker-bootstrap.sh worker &
/app/docker/docker-bootstrap.sh beat &

/app/docker/docker-bootstrap.sh app-gunicorn
