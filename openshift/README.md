# Openshift

## Grant Developer's access
* Create the edit/admin RoleBinding for developers GitHub account, 
  - kind: User
    apiGroup: rbac.authorization.k8s.io
    name: <github username>@github
    
## Add role to group otherwise dev, test and prod can't pull images from tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:30b186-dev -n 30b186-tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:30b186-test -n 30b186-tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:30b186-prod -n 30b186-tools

## Keycloak
openshift/templates/keycloak/keycloak-setcret.yaml

## Minio

## Patroni

## Backend

## Frontend

