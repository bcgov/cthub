FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset
USER root
RUN pip install psycopg2-binary sqlalchemy-redshift \
    && chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home
COPY ./scripts /app/docker
USER superset