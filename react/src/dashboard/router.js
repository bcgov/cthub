import React from 'react';
import { Route } from 'react-router-dom';

import DashboardContainer from './DashboardContainer';

const Router = () => (
  <>
    <Route
      exact
      path="/"
      component={DashboardContainer}
    />
  </>
);

export default Router;
