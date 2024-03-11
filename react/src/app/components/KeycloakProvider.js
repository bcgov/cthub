import React, { useState, useEffect } from 'react'
import { KeycloakContext } from '../../contexts'
import settings from '../settings'

const KeycloakProvider = ({authClient, initOptions, LoadingComponent, children}) => {
  const keycloakEnabled = settings.ENABLE_KEYCLOAK
  const [loading, setLoading] = useState(keycloakEnabled ? true : false)
  const [keycloak, setKeycloak] = useState({})

  useEffect(() => {
    if (keycloakEnabled) {
      authClient.init(initOptions).then(() => {
        setKeycloak(authClient)
        setLoading(false)
      })
    }
  }, [keycloakEnabled, authClient, initOptions])

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