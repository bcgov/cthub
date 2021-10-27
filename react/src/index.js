import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';

import keycloak from './keycloak';
import settings from './app/settings';

import './app/styles/index.scss';

import App from './App';
import Home from './home';

if (settings.ENABLE_KEYCLOAK) {
  ReactDOM.render(
    <>
      <ReactKeycloakProvider
        authClient={keycloak}
        LoadingComponent={(<div>Loading...</div>)}
        isLoadingCheck={(kc) => !kc}
      >
        <App />
      </ReactKeycloakProvider>
    </>,
    document.getElementById('root'),
  );
} else {
  ReactDOM.render(<App />, document.getElementById('root'));
}
