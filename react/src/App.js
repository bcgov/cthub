import 'regenerator-runtime/runtime';
import axios from 'axios';
import React from 'react';
import {
  Redirect,
  Route,
  BrowserRouter as Router,
  Switch,
} from 'react-router-dom';

import settings from './app/settings';
import IcbcDataContainer from './icbc_data/IcbcDataContainer';

const { API_BASE } = settings;

axios.defaults.baseURL = API_BASE;

const App = () => {
  const { sessionStorage } = window;
  const redirect = sessionStorage.getItem('redirect');
  if (redirect && redirect !== '') {
    sessionStorage.removeItem('redirect');
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="container">
          <a href="/">
            <div className="logo" />
          </a>
        </div>
      </header>

      <div className="App-body">
        <Router>
          {redirect && redirect !== '' && (
            <Redirect to={redirect} />
          )}

          <Switch>
            <Route
              path="/"
              component={IcbcDataContainer}
            />
          </Switch>
        </Router>
      </div>
    </div>
  );
};

export default App;
