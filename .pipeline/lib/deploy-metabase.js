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

  const templatesLocalBaseUrl = oc.toFileUrl(path.resolve(__dirname, "../../openshift"));
  var objects = [];

  // The deployment of your cool app goes here ▼▼▼
  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/metabase-postgresql/metabase-dc.yaml`, {
    'param': {
      'ENV_NAME': phases[phase].phase,
      'SUFFIX': phases[phase].suffix,
      'CPU_REQUEST': phases[phase].metabaseCpuRequest,
      'CPU_LIMIT': phases[phase].metabaseCpuLimit,
      'MEMORY_REQUEST': phases[phase].metabaseMemoryRequest,
      'MEMORY_LIMIT': phases[phase].metabaseMemoryLimit,
      'REPLICAS': phases[phase].metabaseReplicas,
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
