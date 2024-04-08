import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Alert } from '@mui/material';
import React, { useState, useEffect, useCallback } from 'react';
import { produce } from 'immer';
import ROUTES_USERS from './routes';
import UsersPage from './components/UsersPage';
import useAxios from '../app/utilities/useAxios';
import AlertDialog from '../app/components/AlertDialog';
import Loading from '../app/components/Loading';

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
  const [openDialog, setOpenDialog] = useState(false);
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
            draft.sort((a, b) => a.idir.localeCompare(b.idir));
          }),
        );
        setNewUser('')
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

  const handleDeleteUserClick = (idir) => {
    setUserToDelete(idir);
    setOpenDialog(true);
  }

  const handleDeleteUser = () => {
    axios.delete(ROUTES_USERS.DETAILS.replace(/:id/g, userToDelete))
      .then((response) => {
        setMessageSeverity('success');
        setMessage(`${userToDelete} was deleted from the user table`);
        setUsers(
          produce((draft) => {
            const indexOfUserToRemove = draft.findIndex((user) => user.idir === userToDelete);
            draft.splice(indexOfUserToRemove, 1);
          }),
        );
      })
      .catch((error) => {
        setMessageSeverity('error');
        setMessage('something went wrong when deleting the user, sorry!');
      })
      .finally(() => {
        setUserToDelete('');
        setOpenDialog(false)
      });
  }

  const handleDeleteUserCancel = () => {
    setUserToDelete('');
    setOpenDialog(false);
  }

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

  useEffect(() => {
    setLoading(true);
    axios.get(ROUTES_USERS.LIST).then((listResponse) => {
      setUsers(listResponse.data);
    });
    setLoading(false);
  }, []);

  if (loading) {
    return <Loading />
  }
  return (
    <div className="users-container">
      {message && <Alert severity={messageSeverity}>{message}</Alert>}
        <AlertDialog
          open={openDialog}
          title={'Delete user?'}
          dialogue={`${userToDelete} will be removed from the application and will have no permissions.`}
          cancelText={'Cancel'}
          handleCancel={handleDeleteUserCancel}
          confirmText={'Delete'}
          handleConfirm={handleDeleteUser}
        />
      <UsersPage
        currentUser={currentUser}
        users={users}
        setNewUser={setNewUser}
        handleAddNewUser={handleAddNewUser}
        handleCheckboxChange={handleCheckboxChange}
        handleSubmitUserUpdates={handleSubmitUserUpdates}
        setMessage={setMessage}
        newUser={newUser}
        handleXClick={handleDeleteUserClick}
      />
    </div>
  );
};
UsersContainer.propTypes = {
  currentUser: PropTypes.string.isRequired,
};
export default withRouter(UsersContainer);
