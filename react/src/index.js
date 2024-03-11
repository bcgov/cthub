import React from 'react';
import ReactDOM from 'react-dom'
import Keycloak from 'keycloak-js';

import KeycloakProvider from './app/components/KeycloakProvider';
import App from './App';
import Loading from './app/components/Loading';

import './app/styles/index.scss';

const keycloak = new Keycloak()
const keycloakInitOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
}

ReactDOM.render(
  <KeycloakProvider
    authClient={keycloak}
    initOptions={keycloakInitOptions}
    LoadingComponent={Loading}
  >
    <App />
  </KeycloakProvider>,
  document.getElementById('root')
)
