import 'regenerator-runtime/runtime';
import axios from 'axios';
import React from 'react';
import { Switch } from 'react-router';
import { Route, BrowserRouter } from 'react-router-dom';

import CustomPropTypes from './app/utilities/props';
import settings from './app/settings';
import IcbcDataContainer from './icbc_data/IcbcDataContainer';

const { API_BASE } = settings;

axios.defaults.baseURL = API_BASE;

const App = (props) => {
  const { keycloak } = props;

  keycloak.onTokenExpired = () => {
    keycloak.updateToken(5).then((refreshed) => {
      if (refreshed) {
        const { token: newToken } = keycloak;

        axios.defaults.headers.common.Authorization = `Bearer ${newToken}`;
      }
    }).catch(() => {
      keycloak.logout();
    });
  };

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

App.propTypes = {
  keycloak: CustomPropTypes.keycloak.isRequired,
};

export default App;
