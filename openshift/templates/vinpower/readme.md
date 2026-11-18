# readme file how to deploy vinpower on Openshift
cthub has adopted the quickstart template but vinpower is left over because it need to a jar file from artifactory

# always uninstall vinpower first when release to test and prod env

# command to create build config on Openshift
oc process -f ./vinpower-bc.yml NAME=cthub SUFFIX=-0.7.0 VERSION=0.7.0 GIT_URL=https://github.com/bcgov/cthub GIT_REF=v0.7.0 | oc apply -f - -n <namespace-plate>-tools

# command to tage to dev, test and prod
oc tag <namespace-plate>-tools/cthub-vinpower:0.7.0 <namespace-plate>-<env>/cthub-vinpower:0.7.0

# Update the tag in CD Repo

