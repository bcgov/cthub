import React from 'react';
import { Route } from 'react-router-dom';

import UploadContainer from './UploadContainer';

const Router = () => (
  <>
    <Route
      exact
      path="/upload"
      component={UploadContainer}
    />
  </>
);

export default Router;
