import React, { useState, useEffect } from 'react'
import { KeycloakContext } from '../../contexts'
import { ENABLE_KEYCLOAK } from '../../config'

const KeycloakProvider = ({authClient, initOptions, LoadingComponent, children}) => {
  const [loading, setLoading] = useState(ENABLE_KEYCLOAK ? true : false)
  const [keycloak, setKeycloak] = useState({})

  useEffect(() => {
    if (ENABLE_KEYCLOAK) {
      authClient.init(initOptions).then(() => {
        setKeycloak(authClient)
        setLoading(false)
      })
    }
  }, [authClient, initOptions])

  if (loading) {
    return <LoadingComponent/>
  }
  return (
    <KeycloakContext.Provider value={keycloak}>
      {children}
    </KeycloakContext.Provider>
  )
}

export default KeycloakProvider