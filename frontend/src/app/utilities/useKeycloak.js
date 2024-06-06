import { useContext } from "react";
import { KeycloakContext } from "../../contexts";

const useKeycloak = () => {
  const keycloak = useContext(KeycloakContext);
  return keycloak;
};

export default useKeycloak;
