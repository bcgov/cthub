FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest-dev
ARG SUPERSET_COMMAND
USER 1001
ENTRYPOINT ["/app/docker/docker-bootstrap.sh", "$SUPERSET_COMMAND"]