import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';

import Login from './Login';
import App from './App';

const keycloakContainer = () => {
  const [auth, setAuth] = useState({ keycloak: {} });
  const keycloakJson = window.location.hostname === 'localhost'
    ? '/keycloak-local.json'
    : '/keycloak.json';
  const keycloak = Keycloak(keycloakJson);
  const initOptions = { pkceMethod: 'S256', redirectUri: `${window.location.origin}/`, idpHint: 'idir' };

  useEffect(() => {
    const initKeycloak = async () => {
      keycloak.init(initOptions).then((authenticated) => {
        setAuth({
          authenticated,
          keycloak,
        });
      });
    };
    initKeycloak();
  }, []);

  if (!keycloak || !auth.keycloak) {
    return <div>Loading...</div>;
  }

  if (!auth.keycloak.authenticated) {
    return <Login keycloak={auth.keycloak} />;
  }

  const { token } = auth.keycloak;
  axios.defaults.headers.common.Authorization = `Bearer ${token}`;

  return (
    <App keycloak={auth.keycloak} />
  );
};

export default keycloakContainer;
