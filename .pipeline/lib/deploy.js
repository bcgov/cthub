"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");
const path = require("path");
//const KeyCloakClient = require('./keycloak');

module.exports = settings => {
  const phases = settings.phases;
  const options = settings.options;
  const phase = options.env;
  const changeId = phases[phase].changeId;
  const oc = new OpenShiftClientX(Object.assign({namespace: phases[phase].namespace}, options));

  //add Valid Redirect URIs for the pull request to keycloak
  /************
  if(phase === 'dev') {
    const kc = new KeyCloakClient(settings, oc);
    kc.addUris();
  }
  *************/

  const templatesLocalBaseUrl = oc.toFileUrl(path.resolve(__dirname, "../../openshift"));
  var objects = [];

  // The deployment of your cool app goes here ▼▼▼

  //create network security policies for internal pod to pod communications
  if(phase === 'dev') {

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/knp/knp-env-pr.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix,
        'ENVIRONMENT': phases[phase].phase
      }
    }))

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni-2.1.1/templates/prerequisite.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix
      }
    }))

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni-2.1.1/templates/deploy.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix,
        'CPU_REQUEST': phases[phase].patroniCpuRequest,
        'CPU_LIMIT': phases[phase].patroniCpuLimit,
        'MEMORY_REQUEST': phases[phase].patroniMemoryRequest,
        'MEMORY_LIMIT': phases[phase].patroniMemoryLimit,
        'REPLICAS': phases[phase].patroniReplica,
        'PVC_SIZE': phases[phase].patroniPvcSize,
        'STORAGE_CLASS': phases[phase].storageClass
      }
    }))
  }

  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/frontend/frontend-dc.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'ENV_NAME': phases[phase].phase,
      'HOST_NAME': phases[phase].host,
      'CPU_REQUEST': phases[phase].frontendCpuRequest,
      'CPU_LIMIT': phases[phase].frontendCpuLimit,
      'MEMORY_REQUEST': phases[phase].frontendMemoryRequest,
      'MEMORY_LIMIT': phases[phase].frontendMemoryLimit,
      'REPLICAS':  phases[phase].frontendReplicas
    }
  }))
  
  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/backend/backend-dc.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'ENV_NAME': phases[phase].phase,
      'BACKEND_HOST_NAME': phases[phase].backendHost,
      'CPU_REQUEST': phases[phase].backendCpuRequest,
      'CPU_LIMIT': phases[phase].backendCpuLimit,
      'MEMORY_REQUEST': phases[phase].backendMemoryRequest,
      'MEMORY_LIMIT': phases[phase].backendMemoryLimit,
      'HEALTH_CHECK_DELAY': phases[phase].backendHealthCheckDelay,
      'REPLICAS':  phases[phase].backendReplicas
    }
  })) 

  oc.applyRecommendedLabels(
      objects,
      phases[phase].name,
      phase,
      `${changeId}`,
      phases[phase].instance,
  );
  oc.importImageStreams(objects, phases[phase].tag, phases.build.namespace, phases.build.tag);
  oc.applyAndDeploy(objects, phases[phase].instance);

};
