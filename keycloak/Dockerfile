FROM mihaibob/keycloak:18.0.2-legacy

COPY realm.json /tmp/realm.json

ENV KEYCLOAK_USER admin
ENV KEYCLOAK_PASSWORD admin

ENV KEYCLOAK_IMPORT /tmp/realm.json

RUN /opt/jboss/keycloak/bin/add-user-keycloak.sh -r Demo -u user -p 1234