'use strict';
const options= require('@bcgov/pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const version = '1.0.0'
const name = 'cthub'
const ocpName = 'apps.silver.devops'

//if work directly on bcgov repo, the value is bcgov
//if work on forked developer repo, the value is the developer's GitHub Id
//without this line of code, the pr deployment cann't removed when the pr is closed

/*
Resource usage base:

Name        CPU         Memory
backend     40m          520M
frontend    70m         500M
superset    1m          180M
metabase    130m         820M
patroni     70m         410M
redis       2m          20M
Minio       3m          150M
backup      1m          20M

Set the cpu usage 20m as the lowest
Set the limit as two times of request

*/
options.git.owner='bcgov'

const phases = {

  build: {namespace:'30b186-tools'   , transient:true, name: `${name}`, phase: 'build', 
          changeId:`${changeId}`, suffix: `-build-${changeId}`  , instance: `${name}-build-${changeId}`, 
          version:`${version}-${changeId}`, tag:`build-${version}-${changeId}`, ocpName: `${ocpName}`},

  dev: {namespace:'30b186-dev', transient:true, name: `${name}`, ssoSuffix:'-dev', 
        ssoName:'dev.oidc.gov.bc.ca', phase: 'dev'  , changeId:`${changeId}`, suffix: `-dev-${changeId}`, 
        instance: `${name}-dev-${changeId}`  , version:`${version}-${changeId}`, tag:`dev-${version}-${changeId}`, 
        host: `cthub-dev-${changeId}.${ocpName}.gov.bc.ca`, djangoDebug: 'True', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        frontendCpuRequest: '400m', frontendCpuLimit: '800m', frontendMemoryRequest: '600Mi', frontendMemoryLimit: '1200Mi', frontendReplicas: 1,
        backendCpuRequest: '50m', backendCpuLimit: '100m', backendMemoryRequest: '520Mi', backendMemoryLimit: '1Gi', backendHealthCheckDelay: 30, backendHost: `cthub-backend-dev-${changeId}.${ocpName}.gov.bc.ca`, backendReplicas: 1,
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3Gi',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '1G', rabbitmqReplica: 1, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '400m', patroniMemoryRequest: '250Mi', patroniMemoryLimit: '500Mi', patroniPvcSize: '2G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`},

  test: {namespace:'30b186-test', name: `${name}`, ssoSuffix:'-test', 
        ssoName:'test.oidc.gov.bc.ca', phase: 'test'  ,  changeId:`${changeId}`, suffix: `-test`, 
        instance: `${name}-test`, version:`${version}`, tag:`test-${version}`, 
        host: `cthub-test.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        frontendCpuRequest: '400m', frontendCpuLimit: '800m', frontendMemoryRequest: '600Mi', frontendMemoryLimit: '1200Mi', frontendReplicas: 1, frontendMinReplicas: 1, frontendMaxReplicas: 3,
        backendCpuRequest: '50m', backendCpuLimit: '100m', backendMemoryRequest: '520Mi', backendMemoryLimit: '1Gi', backendHealthCheckDelay: 30, backendReplicas: 1, backendMinReplicas: 1, backendMaxReplicas: 3, backendHost: `cthub-backend-test.${ocpName}.gov.bc.ca`,
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3G',
        schemaspyCpuRequest: '20m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '700M', rabbitmqPvcSize: '1G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '400m', patroniMemoryRequest: '250Mi', patroniMemoryLimit: '500Mi', patroniPvcSize: '5G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`},

  prod: {namespace:'30b186-prod', name: `${name}`, ssoSuffix:'', 
        ssoName:'oidc.gov.bc.ca', phase: 'prod'  , changeId:`${changeId}`, suffix: `-prod`, 
        instance: `${name}-prod`, version:`${version}`, tag:`prod-${version}`, 
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        host: `cthub-prod.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logon7.gov.bc.ca',
        frontendCpuRequest: '400m', frontendCpuLimit: '800m', frontendMemoryRequest: '600Mi', frontendMemoryLimit: '1200Mi', frontendReplicas: 1, frontendMinReplicas: 1, frontendMaxReplicas: 3,
        backendCpuRequest: '50m', backendCpuLimit: '100m', backendMemoryRequest: '520Mi', backendMemoryLimit: '1Gi', backendHealthCheckDelay: 30, backendReplicas: 1, backendMinReplicas: 1, backendMaxReplicas: 3, backendHost: `cthub-backend-prod.${ocpName}.gov.bc.ca`,
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3G',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '400m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '5G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '400m', patroniMemoryRequest: '250Mi', patroniMemoryLimit: '500Mi', patroniPvcSize: '8G', patroniReplica: 3, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`}

};

// This callback forces the node process to exit as failure.
process.on('unhandledRejection', (reason) => {
  console.log(reason);
  process.exit(1);
});

module.exports = exports = {phases, options};
