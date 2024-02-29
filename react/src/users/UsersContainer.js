import { withRouter } from 'react-router-dom';
import axios from 'axios';
import CircularProgress from '@mui/material/CircularProgress';
import React, { useState, useEffect } from 'react';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';

const UsersContainer = () => {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [userUpdates, setUserUpdates] = useState([])

  const refreshDetails = () => {
    setLoading(true);
    axios.get(ROUTES_USERS.LIST).then((listResponse) => {
      setUsers(listResponse.data);
    });
  };

  useEffect(() => {
    refreshDetails();
    setLoading(false);
  }, []);

  const userRow = (user) => {
    const userPerms = { admin: false, uploader: false }
    if (user) {
      user.user_permissions.forEach((permission) => {
        userPerms[permission.description] = true;
      });
    }
    return (
      <div className="row" key={user.idir}>
        <input type="checkbox" checked={userPerms.uploader} />
        <input type="checkbox" checked={userPerms.admin} />
        <span>{user.idir}</span>
      </div>
    );
  };
  if (loading) {
    return (
      <div>
        <CircularProgress color="inherit" />
      </div>
    );
  }
  return (
    <div className="row">
      <div>
        <h1>Admin</h1>
      </div>
      <div className="col-12 mr-2">
        <span>IDIR Username</span>
      </div>
      <span>upload </span>
      <span>admin</span>
      <div>
        {users.map((user) => (
          userRow(user)
        ))}
      </div>
    </div>
  );
};
export default withRouter(UsersContainer);
