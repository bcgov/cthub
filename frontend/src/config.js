export const ENABLE_KEYCLOAK = window.cthub_config
  ? window.cthub_config.REACT_APP_ENABLE_KEYCLOAK
  : process.env.REACT_APP_ENABLE_KEYCLOAK;

export const API_BASE = window.cthub_config
  ? window.cthub_config.REACT_APP_API_BASE
  : process.env.REACT_APP_API_BASE;

export const KEYCLOAK_CLIENT_ID = window.cthub_config
  ? window.cthub_config.REACT_APP_KEYCLOAK_CLIENT_ID
  : process.env.REACT_APP_KEYCLOAK_CLIENT_ID;

export const KEYCLOAK_REALM = window.cthub_config
  ? window.cthub_config.REACT_APP_KEYCLOAK_REALM
  : process.env.REACT_APP_KEYCLOAK_REALM;

export const KEYCLOAK_URL = window.cthub_config
  ? window.cthub_config.REACT_APP_KEYCLOAK_URL
  : process.env.REACT_APP_KEYCLOAK_URL;
