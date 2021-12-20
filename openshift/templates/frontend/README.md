### Files included

    * frontend-bc.yaml frontend build config
    * frontend-dc.yaml frontend deployment config
    * frontend-autoscaler.yaml create backend frontend, it is not in pipeline and needs to run independently

### Before triggering pipeline

1. Create base image for frontend nodejs-14:1-46.1634035772 in tools projects

### After pipeline completes

1. Create autoscaler for frontend
