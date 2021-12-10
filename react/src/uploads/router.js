import React from 'react';
import { Route, Switch } from 'react-router-dom';

import UploadContainer from './UploadContainer';

const Router = () => (
  <Switch>
    <Route
      exact
      path="/upload"
    >
      <UploadContainer />
    </Route>
  </Switch>
);

export default Router;
