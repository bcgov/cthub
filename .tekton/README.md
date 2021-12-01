tkn pipeline start build-cthub \
-w name=shared-data,volumeClaimTemplateFile=./shared-data.yaml \
-p repo-url=https://github.com/bcgov/cthub.git \
-p branch=tekton-0.1.0 \
-p frontend-image=image-registry.openshift-image-registry.svc:5000/30b186-tools/cthub-frontend:frontendtekton \
-p backend-image=image-registry.openshift-image-registry.svc:5000/30b186-tools/cthub-backend:backendtekton \
--use-param-defaults