FROM image-registry.openshift-image-registry.svc:5000/30b186-tools/nodejs-12:1-104
RUN curl --silent -L -o /tmp/oc.tar https://downloads-openshift-console.apps.silver.devops.gov.bc.ca/amd64/linux/oc.tar
WORKDIR /tmp
RUN tar xf oc.tar \
    && ls -l / \
    && ls -l 
USER root
RUN cp oc /bin
USER 1001