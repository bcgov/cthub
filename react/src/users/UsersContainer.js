import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { CircularProgress, Alert } from '@mui/material';
import React, { useState, useEffect, useCallback } from 'react';
import { produce } from 'immer';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';
import useAxios from '../app/utilities/useAxios';
import AlertDialog from '../app/components/AlertDialog';

const UsersContainer = (props) => {
  const {
    currentUser,
  } = props;

  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState('');
  const [message, setMessage] = useState('');
  const [messageSeverity, setMessageSeverity] = useState('');
  const [userToDelete, setUserToDelete] = useState('');
  const [open, setOpen] = useState(false);
  const axios = useAxios();

  const handleAddNewUser = () => {
    axios.post(ROUTES_USERS.CREATE, { idir: newUser })
      .then((response) => {
        const userAdded = response.data.idir;
        setMessageSeverity('success');
        setMessage(`${userAdded} was added to the user list`);
        const userObject = { idir: userAdded, user_permissions: { admin: false, uploader: false } };
        setUsers(
          produce((draft) => {
            draft.push(userObject);
          }),
        );
      })
      .catch((error) => {
        setMessageSeverity('error');
        setMessage('new user could not be added, sorry!');
      });
  };
  const handleCheckboxChange = useCallback((event) => {
    setMessage('');
    const idir = event.target.name;
    const permissionType = event.target.id;
    const { checked } = event.target;
    setUsers(
      produce((draft) => {
        const userToChange = draft.find((user) => user.idir === idir);
        userToChange.user_permissions[permissionType] = checked;
      }),
    );
  }, []);

  const handleDeleteUser = useCallback((idir) => {
    axios.delete(ROUTES_USERS.DELETE, { data: { current_user: currentUser, idir } })
      .then((response) => {
        setMessageSeverity('success');
        setMessage(`${idir} was deleted from the user table`);
        setUsers(response.data);
      })
      .catch((error) => {
        setMessageSeverity(error);
        setMessage(error.data);
      });
  }, []);

  const handleSubmitUserUpdates = () => {
    axios.put(ROUTES_USERS.UPDATE, users)
      .then((response) => {
        setMessageSeverity('success');
        setMessage(response.data);
      })
      .catch((error) => {
        setMessageSeverity('error');
        setMessage(error.data);
      });
  };

  const handleXClick = (idir) => {
    setMessage('');
    setUserToDelete(idir);
    setOpen(true);
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
    <div className="users-container">
      {message && <Alert severity={messageSeverity}>{message}</Alert>}
      {open && (
        <AlertDialog
          open={open}
          setOpen={setOpen}
          dialogue={`${userToDelete} will be removed from the application and will have no permissions.`}
          rightButtonText="Delete"
          leftButtonText="Cancel"
          title="Delete user?"
          handleDeleteUser={handleDeleteUser}
          userToDelete={userToDelete}
        />
      )}
      <UsersPage
        currentUser={currentUser}
        users={users}
        setNewUser={setNewUser}
        handleAddNewUser={handleAddNewUser}
        handleCheckboxChange={handleCheckboxChange}
        handleSubmitUserUpdates={handleSubmitUserUpdates}
        setMessage={setMessage}
        newUser={newUser}
        handleXClick={handleXClick}
      />
    </div>
  );
};
UsersContainer.propTypes = {
  currentUser: PropTypes.string.isRequired,
};
export default withRouter(UsersContainer);
