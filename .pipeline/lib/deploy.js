"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");
const path = require("path");
const KeyCloakClient = require('./keycloak');

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
  /*
  if(phase === 'dev') {
    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/knp/knp-env-pr.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix,
        'ENVIRONMENT': phases[phase].phase
      }
    }))
  }*/

  if(phase === 'dev') {
    //deploy Patroni required secrets
    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni/prerequisite.yaml`, {
      'param': {
        'NAME': 'patroni',
        'SUFFIX': phases[phase].suffix
      }
    }))
    //deploy Patroni
    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni/deploy.yaml`, {
      'param': {
        'NAME': 'patroni',
        'SUFFIX': phases[phase].suffix,
        'CPU_REQUEST': phases[phase].patroniCpuRequest,
        'CPU_LIMIT': phases[phase].patroniCpuLimit,
        'MEMORY_REQUEST': phases[phase].patroniMemoryRequest,
        'MEMORY_LIMIT': phases[phase].patroniMemoryLimit,
        'IMAGE_REGISTRY': 'image-registry.openshift-image-registry.svc:5000',
        'IMAGE_STREAM_NAMESPACE': phases['build'].namespace,
        'IMAGE_NAME': 'patroni-postgres',
        'IMAGE_TAG': '12.4-20210928',
        'REPLICAS': phases[phase].patroniReplica,
        'PVC_SIZE': phases[phase].patroniPvcSize,
        'STORAGE_CLASS': phases[phase].storageClass
      }
    }))
  }

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
