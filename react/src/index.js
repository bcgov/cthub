import React from 'react';
import ReactDOM from 'react-dom';

import Keycloak from './keycloak';
import settings from './app/settings';

import './app/styles/index.scss';

import App from './App';

if (settings.ENABLE_KEYCLOAK) {
  ReactDOM.render(
    <Keycloak />,
    document.getElementById('root'),
  );
} else {
  ReactDOM.render(<App />, document.getElementById('root'));
}
