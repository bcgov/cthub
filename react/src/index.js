import React from 'react';
import ReactDOM from 'react-dom'
import Keycloak from 'keycloak-js';

import KeycloakProvider from './app/components/KeycloakProvider';
import App from './App';
import Loading from './app/components/Loading';
import Layout from './app/components/Layout';

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
    <Layout>
      <App />
    </Layout>
  </KeycloakProvider>,
  document.getElementById('root')
)
