import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';

import IcbcDataRouter from '../../icbc_data/router';
import UploadRouter from '../../uploads/router';
import DashboardContainer from '../../dashboard/DashboardContainer';
import useKeycloak from '../utilities/useKeycloak'
import Login from './Login'
import Layout from './Layout'
import { ENABLE_KEYCLOAK } from '../../config';

const App = () => {
  const keycloak = useKeycloak()
  
  if (ENABLE_KEYCLOAK && !keycloak.authenticated) {
    const redirectUri = window.location.href
    return <Login redirectUri={redirectUri}/>
  }
  return (
    <Layout>
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
    </Layout>
  );
};

export default App;
