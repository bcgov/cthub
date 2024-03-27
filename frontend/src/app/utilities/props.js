import PropTypes from 'prop-types';

const CustomPropTypes = {
  keycloak: PropTypes.shape({
    authenticated: PropTypes.bool,
    login: PropTypes.func,
    realmAccess: PropTypes.shape({
      roles: PropTypes.arrayOf(PropTypes.string),
    }),
  }),
};

export default CustomPropTypes;
