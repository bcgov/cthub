FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest-dev
USER root
RUN pip install --upgrade pip \
    pip install psycopg2-binary sqlalchemy-redshift \
    && chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home \
    && chgrp -R root /app/superset \
    && chmod -R g+w /app/superset
RUN mkdir /app/docker
COPY ./scripts /app/docker
ENTRYPOINT ["/app/docker/docker-bootstrap.sh"]
CMD ["app-gunicorn"]