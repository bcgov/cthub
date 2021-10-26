import Keycloak from 'keycloak-js';

import settings from './app/settings';

const keycloak = new Keycloak({
  clientId: settings.KEYCLOAK_CLIENT_ID,
  realm: settings.KEYCLOAK_REALM,
  url: settings.KEYCLOAK_URL,
});

export default keycloak;
