import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';

import Login from './Login';
import App from './App';

const keycloakContainer = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [initializedKeycloak, setInitializedKeycloak] = useState(false);
  let globalTimeout;

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

  const refreshToken = (time = 60) => {
    /*
    the time (in seconds) is used to check whether how long our current token has left,
    if it's less than that, then we can refresh the token. otherwise, just keep reusing
    the current token
    */
    initializedKeycloak.updateToken(time).then((refreshed) => {
      if (refreshed) {
        const { token: newToken } = initializedKeycloak;

        axios.defaults.headers.common.Authorization = `Bearer ${newToken}`;

        clearTimeout(globalTimeout);
        setDelayedRefreshToken();
      }
    }).catch(() => {
      initializedKeycloak.logout();
    });
  };

  const setDelayedRefreshToken = () => {
    globalTimeout = setTimeout(() => {
      refreshToken();
    }, 4 * 60 * 1000); // 4 minutes x 60 seconds x 1000 milliseconds
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

  axios.interceptors.request.use((config) => {
    if (initializedKeycloak.isTokenExpired(150)) { // if the token is expiring by 2 mins, 30 secs
      refreshToken(300); // refresh the token now
    }

    return config;
  }, (error) => (Promise.reject(error)));

  setDelayedRefreshToken();

  return <App />;
};

export default keycloakContainer;
