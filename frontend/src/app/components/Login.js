import React from 'react';
import PropTypes from 'prop-types';
import useKeycloak from '../../app/utilities/useKeycloak';

const Login = (props) => {
  const { redirectUri } = props;
  const loginOptions = {
    idpHint: 'idir'
  }
  if (redirectUri) {
    loginOptions.redirectUri = redirectUri
  }
  const keycloak = useKeycloak()

  return (
    <div id="login-page">
      <div id="header">
        <div className="text">Clean Transportation Datahub</div>
      </div>
      <div id="main-content">
        <div className="flex-container">
          <div className="brand-logo" />
          <div className="buttons-section">
            <button type="button" onClick={() => keycloak.login(loginOptions)} id="link-idir" className="button">
              <span className="text"> Login with </span>
              <span className="display-name"> IDIR </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

Login.propTypes = {
  redirectUri: PropTypes.string
};

export default Login;
