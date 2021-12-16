FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest-dev
USER root
RUN pip install --upgrade pip \
    pip install -U celery \
    pip install psycopg2-binary sqlalchemy-redshift \
    && chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home \
    && chgrp -R root /var/log/celery /var/run/celery \
    && chmod -R g+w /var/log/celery/ /var/run/celery    
RUN mkdir /app/docker
COPY ./scripts /app/docker
ENTRYPOINT ["/app/docker/docker-bootstrap.sh"]
CMD ["app-gunicorn"]