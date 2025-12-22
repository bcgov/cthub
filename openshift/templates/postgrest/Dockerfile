FROM artifacts.developer.gov.bc.ca/docker-remote/postgrest/postgrest:v14.2 AS postgrest

# RUN apt-get -y update \
#     && apt-get -y install curl

# RUN mkdir /var/run/postgresql \
#     && chgrp -R root /var/run/postgresql \
#     && chmod -R g+w /var/run/postgresql

# Stage 2: small OS base with shell and curl
FROM registry.access.redhat.com/ubi9/ubi-minimal

# Add curl (and CA certs, tini if you want a proper PID 1)
RUN microdnf -y install curl ca-certificates shadow-utils \
 && microdnf -y clean all

# Copy the PostgREST binary (path in the base image can be /usr/local/bin/postgrest)
COPY --from=postgrest /usr/local/bin/postgrest /usr/local/bin/postgrest

# (Optional) copy your config file; or mount it via a Secret/ConfigMap in OpenShift
# COPY postgrest.conf /etc/postgrest.conf

# OpenShift runs containers as arbitrary UIDs by default; ensure writeable dirs
# If you write logs or cache to a path, make the directory group-writable by UID 0 (root group)
# Example:
RUN mkdir -p /var/lib/postgrest && chgrp -R 0 /var/lib/postgrest && chmod -R g+rwX /var/lib/postgrest

# Expose the HTTP port (change if you configured a different one)
EXPOSE 3000

# Set a default command; you can override with args in your Deployment
# If using a config file:
# CMD ["/usr/local/bin/postgrest", "/etc/postgrest.conf"]
# Or with env-only config (PGRST_* vars):
CMD ["/usr/local/bin/postgrest"]


USER 1001