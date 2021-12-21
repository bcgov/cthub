FROM artifacts.developer.gov.bc.ca/docker-remote/apache/superset:latest
USER root
# RUN pip install --upgrade pip \
#    pip install psycopg2-binary sqlalchemy-redshift
RUN chgrp -R root /app/superset_home \
    && chmod -R g+w /app/superset_home
RUN mkdir /app/docker
COPY ./scripts /app/docker
ENTRYPOINT ["/app/docker/docker-bootstrap.sh"]
CMD ["app-gunicorn"]