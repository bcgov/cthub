"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");

// The clean tasks should be based on the following five labels added by BCDK pipeline
// app: cthub-dev-45
// template-hash: 5ee0ba9e32efa8ac4d0ed2b9923ea2be3ddda2f4
// github-owner: bcgov
// env-name: dev
// app.kubernetes.io/component: database
// app.kubernetes.io/managed-by: template
// app-name: cthub
// app.kubernetes.io/name: patroni
// env-id: '45'
// github-repo: cthub

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
  const github_repo = oc.git.repository.substr(oc.git.repository.lastIndexOf("/")+1);
  
  console.log("github_repo=${github_repo}");

  target_phases.forEach(k => {

    //k is dve, test or prod
    if (phases.hasOwnProperty(k)) {

      const phase = phases[k];
      oc.namespace(phase.namespace);

      let deploymentConfigs = oc.get("dc", {
        selector: `app=${phase.instance},env-id=${phase.changeId},env-name=${k},!shared,github-repo=${github_repo},github-owner=${oc.git.owner}`,
        namespace: phase.namespace,
      });
      deploymentConfigs.forEach(dc => {
        dc.spec.triggers.forEach(trigger => {
          if (
              trigger.type == "ImageChange" &&
              trigger.imageChangeParams.from.kind == "ImageStreamTag"
          ) {
            oc.delete([`ImageStreamTag/${trigger.imageChangeParams.from.name}`], {
              "ignore-not-found": "true",
              wait: "true",
              namespace: phase.namespace,
            });
          }
        });
        oc.delete([`DeploymentConfig/${dc.metadata.name}`], {
          "ignore-not-found": "true",
          wait: "true",
          namespace: phase.namespace,
        });
      });
      oc.raw(
        "delete",
        ["Secret,configmap,endpoints,RoleBinding,role,ServiceAccount,Endpoints,service,route"],
        {
          selector: `app=${phase.instance},env-id=${phase.changeId},!shared,github-repo=${github_repo},github-owner=${oc.git.owner}`,
          wait: "true",
          namespace: phase.namespace,
        }
      );

      //get all statefulsets before they are deleted
      const statefulsets = oc.get("statefulset", {
        selector: `app=${phase.instance},env-id=${phase.changeId},!shared,github-repo=${github_repo},github-owner=${oc.git.owner}`,
        namespace: phase.namespace,
      });   
      //remove all the PVCs associated with each statefulset, after they get deleted by above delete all operation
      statefulsets.forEach(statefulset => {
        //delete StatefulSet
        oc.delete([`StatefulSet/${statefulset.metadata.name}`], {
          "ignore-not-found": "true",
          wait: "true",
          namespace: phase.namespace,
        });        
        //delete configmaps create by patroni
        let patroniConfigmaps = oc.get("configmap", {
          selector: `app.kubernetes.io/name=patroni,cluster-name=${statefulset.metadata.name}`,
          namespace: phase.namespace,
        });
        if(Object.entries(patroniConfigmaps).length > 0) {
          oc.raw(
            "delete",
            ["configmap"],
            {
              selector: `app.kubernetes.io/name=patroni,cluster-name=${statefulset.metadata.name}`,
              wait: "true",
              "ignore-not-found": "true",
              namespace: phase.namespace,
            },
          );        
        };
        //delete PVCs mounted for statfulset
        oc.raw("delete", ["pvc"], {
          selector: `app=${phase.instance},statefulset=${statefulset.metadata.name},!shared,github-repo=${oc.git.repository},github-owner=${oc.git.owner}`,
          "ignore-not-found": "true",
          wait: "true",
          namespace: phase.namespace,
        });

      });

      //remove all PR's network policies
      const knps = oc.get("networkpolicies", {
        selector: `app=${phase.instance},env-id=${phase.changeId},env-name=${k},!shared,github-repo=${github_repo},github-owner=${oc.git.owner}`,
        namespace: phase.namespace,
      });   
      knps.forEach(knp => {
        oc.delete([`networkpolicy/${knp.metadata.name}`], {
            "ignore-not-found": "true",
            wait: "true",
            namespace: phase.namespace,
          });       
      });

    }
  });
};
