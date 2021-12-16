FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest-dev
ARG SUPERSET_COMMAND
USER root
RUN pip install psycopg2-binary sqlalchemy-redshift \
    && chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home
COPY ./scripts /app/docker
USER superset
ENTRYPOINT ["/app/docker/docker-bootstrap.sh", "$SUPERSET_COMMAND"]