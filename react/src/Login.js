import React from 'react';
import CustomPropTypes from './app/utilities/props';

const Login = (props) => {
  const { keycloak } = props;
  return (
    <div id="login-page">
      <div id="header">
        <div className="text">Clean Transportation Datahub</div>
      </div>
      <div id="main-content">
        <div className="flex-container">
          <div className="brand-logo" />
          <div className="buttons-section">
            <button type="button" onClick={() => keycloak.login({ idpHint: 'idir' })} id="link-idir" className="button">
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
  keycloak: CustomPropTypes.keycloak.isRequired,
};

export default Login;
