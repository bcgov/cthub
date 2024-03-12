import 'regenerator-runtime/runtime';
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';

import settings from './app/settings';
import IcbcDataRouter from './icbc_data/router';
import UploadRouter from './uploads/router';
import DashboardContainer from './dashboard/DashboardContainer';
import useKeycloak from './app/utilities/useKeycloak'
import Login from './Login';

const { ENABLE_KEYCLOAK } = settings;

const App = () => {
  const keycloak = useKeycloak()
  
  if (ENABLE_KEYCLOAK && !keycloak.authenticated) {
    const redirectUri = window.location.href
    return <Login redirectUri={redirectUri}/>
  }
  return (
    <div className="App">
      <div className="App-body">
        <Router>
          <Switch>
            {IcbcDataRouter()}
            {UploadRouter()}
            <Route>
              <DashboardContainer />
            </Route>
          </Switch>
        </Router>
      </div>
    </div>
  );
};

export default App;
