"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");

// The clean tasks should be based on the following five labels added by BCDK pipeline
// namespace: '30b186-tools',
// transient: true,
// name: 'cthub',
// phase: 'build',
// changeId: '46',
// suffix: '-build-46',
// instance: 'cthub-build-46',
// version: '1.0.0-46',
// tag: 'build-1.0.0-46',
// ocpName: 'apps.silver.devops'

const getTargetPhases = (env, phases) => {
  let target_phase = [];
  for (const phase in phases) {
    if (env.match(/^(all|transient)$/) && phases[phase].transient) {
      target_phase.push(phase);
    } else if (env === phase) {
      target_phase.push(phase);
      break;
    }
  }

  return target_phase;
};

module.exports = settings => {
  const phases = settings.phases;
  const options = settings.options;
  const oc = new OpenShiftClientX(Object.assign({ namespace: phases.build.namespace }, options));
  const target_phases = getTargetPhases(options.env, phases);

  target_phases.forEach(k => {
    if (phases.hasOwnProperty(k)) {

      const phase = phases[k];
      oc.namespace(phase.namespace);

      let buildConfigs = oc.get("bc", {
        selector: `app=${phase.instance},env-id=${phase.changeId},!shared,github-repo=${oc.git.repository},github-owner=${oc.git.owner}`,
        namespace: phase.namespace,
      });

      buildConfigs.forEach(bc => {
        if (bc.spec.output.to.kind == "ImageStreamTag") {
          oc.delete([`ImageStreamTag/${bc.spec.output.to.name}`], {
            "ignore-not-found": "true",
            wait: "true",
            namespace: phase.namespace,
          });
        }
        oc.delete([`BuildConfig/${bc.metadata.name}`], {
          "ignore-not-found": "true",
          wait: "true",
          namespace: phase.namespace,
        });        
      });

    }
  });
};
