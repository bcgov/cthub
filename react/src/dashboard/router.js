import React from 'react';
import { Route } from 'react-router-dom';

import DashboardContainer from './DashboardContainer';

const Router = () => (
  <>
    <Route
      path="/"
      component={DashboardContainer}
    />
  </>
);

export default Router;
