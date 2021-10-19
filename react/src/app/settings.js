/* global
  __API_BASE__,
  __ENABLE_KEYCLOAK__,
  __KEYCLOAK_URL__,
*/
import { useKeycloak as reactKeycloak } from '@react-keycloak/web';

let useKeycloak;

if (__ENABLE_KEYCLOAK__) {
  useKeycloak = reactKeycloak;
} else {
  useKeycloak = () => ({ // mock useKeycloak
    keycloak: {
      authenticated: true,
      token: '',
    },
    initialized: true,
  });
}

const settings = {
  API_BASE: __API_BASE__,
  ENABLE_KEYCLOAK: __ENABLE_KEYCLOAK__,
  KEYCLOAK_URL: __KEYCLOAK_URL__,
  useKeycloak,
};

export default settings;
