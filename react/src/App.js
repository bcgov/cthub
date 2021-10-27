import 'regenerator-runtime/runtime';
import axios from 'axios';
import React from 'react';
import { Switch } from 'react-router';
import { Route, BrowserRouter } from 'react-router-dom';
import Login from './Login';

import settings from './app/settings';
import IcbcDataContainer from './icbc_data/IcbcDataContainer';

const { API_BASE, useKeycloak } = settings;

axios.defaults.baseURL = API_BASE;

const App = () => {
  const { keycloak } = useKeycloak();

  if (keycloak && !keycloak.authenticated) {
    return <Login keycloak={keycloak} />;
  }

  const { token } = keycloak;
  axios.defaults.headers.common.Authorization = `Bearer ${token}`;

  return (
    <div className="App">
      <header className="App-header">
        <div className="container">
          <a href="/">
            <div className="logo" />
          </a>
        </div>
      </header>

      <div className="App-body">
        <BrowserRouter>
          <Switch>
            <Route
              path="/"
              component={IcbcDataContainer}
            />
          </Switch>
        </BrowserRouter>
      </div>
    </div>
  );
};

export default App;
