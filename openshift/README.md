# Openshift

## Grant Developer's access
* Create the edit/admin RoleBinding for developers GitHub account, 
  - kind: User
    apiGroup: rbac.authorization.k8s.io
    name: <github username>@github

