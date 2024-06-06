import React from "react";
import useKeycloak from "../utilities/useKeycloak";

const Logout = () => {
  const keycloak = useKeycloak();
  if (keycloak.authenticated) {
    const kcToken = keycloak.tokenParsed;
    return (
      <div className="logout">
        <span>{"Logged in as: " + kcToken.idir_username + " |"}</span>
        <button
          className="logoutButton"
          onClick={() => {
            keycloak.logout();
          }}
        >
          Log out
        </button>
      </div>
    );
  }
  return null;
};

export default Logout;
