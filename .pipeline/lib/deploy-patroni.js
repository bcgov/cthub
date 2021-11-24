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
