import React from 'react';
import useKeycloak from '../utilities/useKeycloak'

const Logout = () => {
  const keycloak = useKeycloak();
  if (keycloak.authenticated) {
    return (
      <button
        onClick={() => {
          keycloak.logout()
        }}
      >
        Log out
      </button>
    )
  }
  return null
}

export default Logout
