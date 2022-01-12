FROM image-registry.openshift-image-registry.svc:5000/30b186-tools/nodejs-12:1-104
RUN curl --silent -L -o /tmp/oc.tar.gz https://mirror.openshift.com/pub/openshift-v4/clients/oc/4.6.0-202005061824.git.1.7376912.el7/linux/oc.tar.gz
WORKDIR /tmp
RUN gunzip oc.tar.gz \
    && tar xf oc.tar \
    && ls -l / \
    && ls -l 
USER root
RUN cp oc /bin
USER 1001