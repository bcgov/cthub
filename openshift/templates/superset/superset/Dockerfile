FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest-dev
USER root
RUN pip install psycopg2-binary sqlalchemy-redshift \
    && chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home
RUN mkdir /app/docker
RUN ls -l / \
    && ls -l /app \
    && ls -l /app/docker
COPY ./scripts /app/docker
RUN ls -l /app/docker
USER superset
ENTRYPOINT ["/app/docker/docker-bootstrap.sh"]
CMD ["app-gunicorn"]