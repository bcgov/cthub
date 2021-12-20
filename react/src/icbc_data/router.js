import React from 'react';
import { Route, Switch } from 'react-router-dom';

import IcbcDataContainer from './IcbcDataContainer';

const Router = () => (
  <Switch>
    <Route
      exact
      path="/icbc"
    >
      <IcbcDataContainer />
    </Route>
  </Switch>
);

export default Router;
