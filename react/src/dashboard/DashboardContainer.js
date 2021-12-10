import React from 'react';
import { withRouter, Redirect } from 'react-router-dom';

const DashboardContainer = () => (
  <div className="row">
    <div className="col-12">
      <Redirect to="/upload" />
    </div>
  </div>
);

export default withRouter(DashboardContainer);
