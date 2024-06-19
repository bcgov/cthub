FROM bitnami/postgrest:11.2.2

RUN chmod -R g+w /run \
    && mkdir /run/postgresql \
    && chgrp -R root /run/postgresql \
    && chmod -R g+w /run/postgresql