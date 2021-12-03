'use strict';
const options= require('@bcgov/pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const version = '1.0.0'
const name = 'cthub'
const ocpName = 'apps.silver.devops'

//if work directly on bcgov repo, the value is bcgov
//if work on forked developer repo, the value is the developer's GitHub Id
//without this line of code, the pr deployment cann't removed when the pr is closed
options.git.owner='bcgov'

const phases = {

  build: {namespace:'30b186-tools'   , transient:true, name: `${name}`, phase: 'build', 
          changeId:`${changeId}`, suffix: `-build-${changeId}`  , instance: `${name}-build-${changeId}`, 
          version:`${version}-${changeId}`, tag:`build-${version}-${changeId}`, ocpName: `${ocpName}`},

  dev: {namespace:'30b186-dev', transient:true, name: `${name}`, ssoSuffix:'-dev', 
        ssoName:'dev.oidc.gov.bc.ca', phase: 'dev'  , changeId:`${changeId}`, suffix: `-dev-${changeId}`, 
        instance: `${name}-dev-${changeId}`  , version:`${version}-${changeId}`, tag:`dev-${version}-${changeId}`, 
        host: `cthub-dev-${changeId}.${ocpName}.gov.bc.ca`, djangoDebug: 'True', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '300m', metabaseCpuLimit: '500m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        frontendCpuRequest: '100m', frontendCpuLimit: '700m', frontendMemoryRequest: '300M', frontendMemoryLimit: '4G', frontendReplicas: 1,
        backendCpuRequest: '300m', backendCpuLimit: '600m', backendMemoryRequest: '1G', backendMemoryLimit: '2G', backendHealthCheckDelay: 30, backendHost: `cthub-backend-dev-${changeId}.${ocpName}.gov.bc.ca`, backendReplicas: 1,
        minioCpuRequest: '100m', minioCpuLimit: '200m', minioMemoryRequest: '200M', minioMemoryLimit: '500M', minioPvcSize: '1G',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '1G', rabbitmqReplica: 1, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '400m', patroniMemoryRequest: '250M', patroniMemoryLimit: '500M', patroniPvcSize: '2G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`},

  test: {namespace:'30b186-test', name: `${name}`, ssoSuffix:'-test', 
        ssoName:'test.oidc.gov.bc.ca', phase: 'test'  ,  changeId:`${changeId}`, suffix: `-test`, 
        instance: `${name}-test`, version:`${version}`, tag:`test-${version}`, 
        host: `cthub-test.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500M', metabaseMemoryLimit: '2G', metabaseReplicas: 2,
        frontendCpuRequest: '200m', frontendCpuLimit: '400m', frontendMemoryRequest: '500M', frontendMemoryLimit: '2G', frontendReplicas: 2, frontendMinReplicas: 2, frontendMaxReplicas: 5,
        backendCpuRequest: '200m', backendCpuLimit: '500m', backendMemoryRequest: '500M', backendMemoryLimit: '2G', backendHealthCheckDelay: 30, backendReplicas: 2, backendMinReplicas: 2, backendMaxReplicas: 5, backendHost: `cthub-backend-test.${ocpName}.gov.bc.ca`,
        minioCpuRequest: '100m', minioCpuLimit: '300m', minioMemoryRequest: '500M', minioMemoryLimit: '700M', minioPvcSize: '3G',
        schemaspyCpuRequest: '20m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '700M', rabbitmqPvcSize: '1G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '400m', patroniMemoryRequest: '250M', patroniMemoryLimit: '500M', patroniPvcSize: '5G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`},

  prod: {namespace:'30b186-prod', name: `${name}`, ssoSuffix:'', 
        ssoName:'oidc.gov.bc.ca', phase: 'prod'  , changeId:`${changeId}`, suffix: `-prod`, 
        instance: `${name}-prod`, version:`${version}`, tag:`prod-${version}`, 
        metabaseCpuRequest: '200m', metabaseCpuLimit: '400m', metabaseMemoryRequest: '750Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 2,
        host: `cthub-prod.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logon7.gov.bc.ca',
        frontendCpuRequest: '300m', frontendCpuLimit: '600m', frontendMemoryRequest: '1G', frontendMemoryLimit: '2G', frontendReplicas: 2, frontendMinReplicas: 2, frontendMaxReplicas: 5,
        backendCpuRequest: '200m', backendCpuLimit: '700m', backendMemoryRequest: '1G', backendMemoryLimit: '2G', backendHealthCheckDelay: 30, backendReplicas: 2, backendMinReplicas: 2, backendMaxReplicas: 5, backendHost: `cthub-backend-prod.${ocpName}.gov.bc.ca`,
        minioCpuRequest: '100m', minioCpuLimit: '300m', minioMemoryRequest: '500M', minioMemoryLimit: '700M', minioPvcSize: '3G',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '400m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '5G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '200m', patroniCpuLimit: '500m', patroniMemoryRequest: '300M', patroniMemoryLimit: '800M', patroniPvcSize: '8G', patroniReplica: 3, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`}

};

// This callback forces the node process to exit as failure.
process.on('unhandledRejection', (reason) => {
  console.log(reason);
  process.exit(1);
});

module.exports = exports = {phases, options};
