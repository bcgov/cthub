import React from 'react';
import { Route } from 'react-router-dom';

import UploadContainer from './UploadContainer';

const Router = () => ([
  <Route
    exact
    key="route-upload"
    path="/upload"
  >
    <UploadContainer />
  </Route>,
]);

export default Router;
