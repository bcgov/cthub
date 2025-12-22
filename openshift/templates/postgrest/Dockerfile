
# Stage 1: get official PostgREST binary
FROM artifacts.developer.gov.bc.ca/docker-remote/postgrest/postgrest:v14.2 AS postgrest

# Stage 2: UBI9 minimal with a shell and curl-minimal preinstalled
FROM registry.access.redhat.com/ubi9/ubi-minimal

# Install tools:
# - ca-certificates: TLS CA bundle
# - shadow-utils: user/group tooling (handy with OpenShift arbitrary UID)
# - procps-ng: provides `ps`
# - iproute: provides `ss`
# Keep curl-minimal (already present in UBI); don't install full `curl` unless needed.
RUN microdnf -y update \
 && microdnf -y install ca-certificates shadow-utils procps-ng iproute \
 && microdnf -y clean all

# For x86-64 (Nix-based image)
COPY --from=postgrest /bin/postgrest /usr/local/bin/postgrest

# If you build arm64 later, use:
# COPY --from=postgrest /usr/bin/postgrest /usr/local/bin/postgrest


# (Optional) copy your config or mount via ConfigMap/Secret in OpenShift
# COPY postgrest.conf /etc/postgrest.conf

# Make any writable dirs OpenShift-friendly (arbitrary UID)
RUN mkdir -p /var/lib/postgrest \
 && chgrp -R 0 /var/lib/postgrest \
 && chmod -R g+rwX /var/lib/postgrest

EXPOSE 3000

# If you use a config file:
# CMD ["/usr/local/bin/postgrest", "/etc/postgrest.conf"]

# If you configure via env vars (PGRST_*), just run the binary:
CMD ["/usr/local/bin/postgrest"]
