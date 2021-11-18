import React from 'react';
import { Route } from 'react-router-dom';

import IcbcDataContainer from './IcbcDataContainer';

const Router = () => (
  <>
    <Route
      exact
      path="/"
      component={IcbcDataContainer}
    />
  </>
);

export default Router;
