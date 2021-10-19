import Keycloak from 'keycloak-js';

import settings from './app/settings';

const keycloak = new Keycloak({
  clientId: 'demo-app',
  realm: 'Demo',
  url: settings.KEYCLOAK_URL,
});

export default keycloak;
