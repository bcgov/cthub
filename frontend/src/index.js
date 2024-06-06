import React from "react";
import ReactDOM from "react-dom";
import Keycloak from "keycloak-js";

import KeycloakProvider from "./app/components/KeycloakProvider";
import App from "./app/components/App";
import Loading from "./app/components/Loading";
import { KEYCLOAK_CLIENT_ID, KEYCLOAK_REALM, KEYCLOAK_URL } from "./config";

import "./app/styles/index.scss";

const keycloak = new Keycloak({
  clientId: KEYCLOAK_CLIENT_ID,
  realm: KEYCLOAK_REALM,
  url: KEYCLOAK_URL,
});
const keycloakInitOptions = {
  onLoad: "check-sso",
  pkceMethod: "S256",
};

ReactDOM.render(
  <KeycloakProvider
    authClient={keycloak}
    initOptions={keycloakInitOptions}
    LoadingComponent={Loading}
  >
    <App />
  </KeycloakProvider>,
  document.getElementById("root"),
);
