FROM bitnami/postgrest:11.2.2

USER 0

RUN apt-get -y install curl

RUN mkdir /var/run/postgresql \
    && chgrp -R root /var/run/postgresql \
    && chmod -R g+w /var/run/postgresql

USER 1001