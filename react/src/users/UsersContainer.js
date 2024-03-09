import { withRouter } from 'react-router-dom';
import axios from 'axios';
import { CircularProgress, Alert } from '@mui/material';
import React, { useState, useEffect } from 'react';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';

const UsersContainer = (props) => {
  const { currentUser } = props;
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState('');
  const [userUpdates, setUserUpdates] = useState({});
  const [permissionMessage, setPermissionMessage] = useState('');
  const [permissionMessageSeverity, setPermissionMessageSeverity] = useState('');
  const refreshDetails = () => {
    setLoading(true);
    axios.get(ROUTES_USERS.LIST).then((listResponse) => {
      setUsers(listResponse.data);
    });
  };

  const handleAddNewUser = () => {
    axios.post(ROUTES_USERS.CREATE, { idir: newUser }).then((response) => {
      if (response.status === 200) {
        refreshDetails();
        setLoading(false);
      }
    });
  };
  const handleCheckboxChange = (event) => {
    const { checked } = event.target;
    if (permissionMessage) {
      setPermissionMessage('');
    }
    const permissionType = event.target.id;
    const userName = event.target.name;
    // find what permissions were originally retrieved for that user from the axios call
    const originalUser = users.find((user) => user.idir === userName);
    const userPermissions = originalUser.user_permissions;
    // update the permissions
    userPermissions[permissionType] = checked;
    setUserUpdates({ ...userUpdates, [userName]: { [permissionType]: checked } });
  };

  const handleSubmitPermissionUpdates = () => {
    axios.put(ROUTES_USERS.UPDATE, userUpdates).then((response) => {
      if (response.status === 201) {
        setPermissionMessageSeverity('success');
      }
      if (response.status === 400) {
        setPermissionMessageSeverity('error');
      }
      setPermissionMessage(response.data);
      refreshDetails();
      setLoading(false);
    });
  };

  useEffect(() => {
    refreshDetails();
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
      {permissionMessage && <Alert severity={permissionMessageSeverity}>{permissionMessage}</Alert>}
      <UsersPage
        currentUser={currentUser}
        users={users}
        setNewUser={setNewUser}
        handleAddNewUser={handleAddNewUser}
        handleCheckboxChange={handleCheckboxChange}
        userUpdates={userUpdates}
        handleSubmitPermissionUpdates={handleSubmitPermissionUpdates}
      />
    </div>
  );
};
export default withRouter(UsersContainer);
