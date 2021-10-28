import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';

import Login from './Login';
import App from './App';

const keycloakContainer = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [initializedKeycloak, setInitializedKeycloak] = useState(false);

  const keycloakJson = window.location.hostname === 'localhost'
    ? '/keycloak-local.json'
    : '/keycloak.json';
  const keycloak = Keycloak(keycloakJson);
  const initOptions = {
    idpHint: 'idir',
    onLoad: 'check-sso',
    pkceMethod: 'S256',
    redirectUri: `${window.location.origin}/`,
  };

  useEffect(() => {
    const initKeycloak = async () => {
      keycloak.init(initOptions).then((auth) => {
        setAuthenticated(auth);
        setInitializedKeycloak(keycloak);
      });
    };
    initKeycloak();
  }, []);

  if (!keycloak || !initializedKeycloak) {
    return <div>Loading...</div>;
  }

  if (!authenticated) {
    return <Login keycloak={initializedKeycloak} />;
  }

  const { token } = initializedKeycloak;
  axios.defaults.headers.common.Authorization = `Bearer ${token}`;

  return (
    <App keycloak={initializedKeycloak} />
  );
};

export default keycloakContainer;
