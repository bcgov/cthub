import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';
import { ReactKeycloakProvider } from '@react-keycloak/web';

const keycloakContainer = (props) => {
  const [auth, setAuth] = useState({ keycloak: {} });
  const keycloak = Keycloak('/keycloak.json');
  const initOptions = { pkceMethod: 'S256', redirectUri: `${window.location.origin}/`, idpHint: 'idir' };

  useEffect(() => {
    const initKeycloak = async () => {
      keycloak
        .init(initOptions)
        .then((authenticated) => {
          console.error('set auth');
          setAuth({
            authenticated,
            keycloak,
          });
        });
    };
    initKeycloak();
  }, []);
  console.error('keycloak');
  console.error(keycloak);

  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      initOptions={initOptions}
      isLoadingCheck={(kc) => {
        console.error('kc');
        console.error(kc);
        if (!kc.authenticated) {
          kc.login({ idpHint: 'idir' });
          return true;
        }

        if (!axios.defaults.headers.common.Authorization) {
          return true;
        }

        return false;
      }}
      LoadingComponent={(<div>Loading...</div>)}
      onTokens={(keycloakTokens) => {
        console.error('auth keycloak');
        console.error(auth.keycloak);
        const { token } = keycloakTokens;

        if (!token || !auth.keycloak.authenticated) {
          return auth.keycloak.login({ idpHint: 'idir' });
        }

        axios.defaults.headers.common.Authorization = `Bearer ${token}`;
        return true;
      }}
    >
      {props.children}
    </ReactKeycloakProvider>
  );
};

export default keycloakContainer;
