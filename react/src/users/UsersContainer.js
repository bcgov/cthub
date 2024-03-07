import { withRouter } from 'react-router-dom';
import axios from 'axios';
import CircularProgress from '@mui/material/CircularProgress';
import React, { useState, useEffect } from 'react';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';

const UsersContainer = () => {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState('')
  const [userUpdates, setUserUpdates] = useState({});

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
    axios.put(ROUTES_USERS.UPDATE, userUpdates).then((response)=>{
      if (response.status === 201) {
        refreshDetails();
        setLoading(false);
      }
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
      <UsersPage
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
