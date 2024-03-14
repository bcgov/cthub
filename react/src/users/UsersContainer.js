import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { CircularProgress, Alert } from '@mui/material';
import React, { useState, useEffect, useCallback } from 'react';
import { produce } from 'immer';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';
import useAxios from '../app/utilities/useAxios';

const UsersContainer = (props) => {
  const { currentUser } = props;
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState('');
  const [permissionMessage, setPermissionMessage] = useState('');
  const [messageSeverity, setMessageSeverity] = useState('');
  const axios = useAxios();

  const handleCheckboxChange = useCallback((event) => {
    const idir = event.target.name;
    const permissionType = event.target.id;
    const { checked } = event.target;
    setUsers(
      produce((draft) => {
        const user = draft.find((user) => user.idir === idir);
        user.user_permissions[permissionType] = checked;
      }),
    );
  }, []);

  const handleAddNewUser = () => {
    axios.post(ROUTES_USERS.CREATE, { idir: newUser })
      .then((response) => {
        const userAdded = response.data.idir;
        setMessageSeverity('success');
        setPermissionMessage(`${userAdded} was added to the user list`);
        const userObject = { idir: userAdded, user_permissions: { admin: false, uploader: false } };
        setUsers(
          produce((draft) => {
            draft.push(userObject);
          }),
        );
      })
      .catch((error) => {
        setMessageSeverity('error');
        setPermissionMessage('new user could not be added, sorry!');
      });
  };

  const handleSubmitPermissionUpdates = () => {
    axios.put(ROUTES_USERS.UPDATE, users)
      .then((response) => {
        setMessageSeverity('success');
        setPermissionMessage(response.data);
      })
      .catch((error) => {
        setMessageSeverity('error');
        setPermissionMessage(error.data);
      });
  };

  useEffect(() => {
    setLoading(true);
    axios.get(ROUTES_USERS.LIST).then((listResponse) => {
      setUsers(listResponse.data);
    });
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div>
        <CircularProgress color="inherit" />
      </div>
    );
  }
  return (
    <div className="row">
      {permissionMessage && <Alert severity={messageSeverity}>{permissionMessage}</Alert>}
      <UsersPage
        currentUser={currentUser}
        users={users}
        setNewUser={setNewUser}
        handleAddNewUser={handleAddNewUser}
        handleCheckboxChange={handleCheckboxChange}
        handleSubmitPermissionUpdates={handleSubmitPermissionUpdates}
      />
    </div>
  );
};
UsersContainer.propTypes = {
  currentUser: PropTypes.string.isRequired,
};
export default withRouter(UsersContainer);
