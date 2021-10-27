import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [auth, setAuth] = useState({ keycloak: {} });
  const [answer, setAnswer] = useState('');

  useEffect(() => {
    const initKeycloak = async () => {
      let Keycloak = require('keycloak-js');
      const keycloak = Keycloak('/keycloak.json');
      if (window && typeof window !== 'object') return;
      keycloak
        .init({ pkceMethod: 'S256', redirectUri: 'https://cthub-dev-9.apps.silver.devops.gov.bc.ca/', idpHint: 'idir' })
        .then((authenticated) => {
          console.error(authenticated);
          setAuth({ keycloak, authenticated });
        });
    };
    initKeycloak();
  }, []);

  const handleLogin = () => auth.keycloak.login({ idpHint: 'idir' });
  const handleLogout = () => auth.keycloak.logout();

  const getSecret = async () => {
    try {
      const headers = auth.keycloak.token ? { Authorization: `Bearer ${auth.keycloak.token}` } : {};
      const response = await axios.get('https://cthub-backend-dev-9.apps.silver.devops.gov.bc.ca/api/icbc-data', { headers });
      setAnswer(`The password is: ${response.data.message}`);
    } catch (err) {
      setAnswer('Failed to fetch resources');
    }
  };

  console.error(auth);

  return (
    <div>
      <h1>A simple Keycloak Configuration</h1>
      <button type="button" onClick={handleLogin}>Login</button>
      <button type="button" onClick={handleLogout}>Logout</button>
      <button type="button" onClick={getSecret}>Get Protected Resources</button>
      <div>
        <div>
          Click on the button
          <em> Get Protected Resources </em>
          to fetch from the API
        </div>
        {' '}
        {answer && <p>{answer}</p>}
      </div>
    </div>
  );
}
