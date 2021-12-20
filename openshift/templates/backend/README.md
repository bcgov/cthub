### Files included
    * backend-bc.yaml backend build config
    * backend-dc.yaml backend deployment config
    * django-secret-template.yaml create template.django-secret, it is not in pipeline and needs to run independently, it is used by backend-dc.yaml
    * backend-autoscaler.yaml create backend autoscaler, it is not in pipeline and needs to run independently

### Prepare for pipeline build and deploy

#### Before triggering pipeline

1. import python base image python-39:1-18.1634036280 to tools project

2. Create template secret template.django-secret

#### After pipeline completes

1. After pipeline completes, create autoscaler for backend
