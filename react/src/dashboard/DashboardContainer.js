import React from 'react';
import { withRouter, useHistory } from 'react-router-dom';

const DashboardContainer = () => {
  const { location } = window;
  const { pathname } = location;
  const history = useHistory();
  return (

    <div className="row">
      <div className="col-12">
        {pathname === '/' && history.push('/upload')}
      </div>
    </div>
  );
};

export default withRouter(DashboardContainer);
