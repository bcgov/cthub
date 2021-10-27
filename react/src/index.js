import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';

import keycloak from './keycloak';
import settings from './app/settings';

import './app/styles/index.scss';

import App from './App';

if (settings.ENABLE_KEYCLOAK) {
  ReactDOM.render(
    <>
      <ReactKeycloakProvider
        authClient={keycloak}
        LoadingComponent={(<div>Loading...</div>)}
        isLoadingCheck={(kc) => (!kc || !axios.defaults.headers.common.Authorization)}
        onTokens={(keycloakTokens) => {
          const { token } = keycloakTokens;

          if (!token || !keycloak.authenticated) {
            return keycloak.login({ idpHint: 'bceid' });
          }

          axios.defaults.headers.common.Authorization = `Bearer ${token}`;
          return true;
        }}
      >
        <App />
      </ReactKeycloakProvider>
    </>,
    document.getElementById('root'),
  );
} else {
  ReactDOM.render(<App />, document.getElementById('root'));
}
