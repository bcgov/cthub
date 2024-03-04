import React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import ClearIcon from '@mui/icons-material/Clear';
import SaveIcon from '@mui/icons-material/Save';
import TextField from '@mui/material/TextField';

const UsersPage = (props) => {
  const { users, userUpdates, setUserUpdates } = props;

  const userRow = (user) => {
    const userPerms = { admin: false, uploader: false };
    user.user_permissions.forEach((permission) => {
      userPerms[permission.description] = true;
    });

    const handleRadioChange = (event) => {
      const { checked } = event.target;
      const permissionType = event.target.id;
      console.log(permissionType);
      console.log(userPerms);
      userPerms[permissionType] = checked;
      console.log(userPerms[permissionType]);
    };
    return (
      <Grid container key={user.idir}>
        <Grid item className="permissions">
          <input type="checkbox" className="checkbox" name="uploader" id="uploader" checked={userPerms.uploader} onChange={(event) => { handleRadioChange(event); }} />
          <input type="checkbox" className="checkbox" name="admin" id="admin" checked={userPerms.admin} onChange={(event) => { handleRadioChange(event); }} />
        </Grid>
        <Grid item width="20%" paddingLeft={2}>
          <span>{user.idir}</span>
        </Grid>
        <Grid item>
          <ClearIcon padding={0} sx={{color: 'red' }} />
        </Grid>
      </Grid>
    );
  };
  return (
    <Paper variant="outlined">
      <Box p={3}>
        <div>
          <h2>Admin</h2>
        </div>
        <Grid container>
          <Box display="flex" flexDirection="row" className="add-user-box" alignItems="center" padding={2} justifyContent="space-evenly">
            <Grid container alignItems="center" justifyContent="space-around">
              <Grid item spacing={3}>
                <h3>
                  IDIR Username
                </h3>
              </Grid>
              <Grid item>
                <TextField className="user-input" type="text" />
              </Grid>
              <Grid item>
                <Button variant="contained" className="button-dark-blue" >
                  Add User
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid container display="flex" flexDirection="column">
          <Box item className="permissions" justifyContent="space-around" display="flex" flexDirection="row" paddingTop={1}>
            <Box>
              <h4>Upload </h4>
            </Box>
            <Box>
              <h4>Admin</h4>
            </Box>
          </Box>
          {users.map((user) => (
            userRow(user)
          ))}
          <Box className="permissions" justifyContent="space-around" display="flex" paddingTop={3} paddingBottom={3}>
            <Button variant="contained" className="button-dark-blue" startIcon={<SaveIcon />}>
              Save
            </Button>
          </Box>
        </Grid>
      </Box>
    </Paper>
  );
};
UsersPage.propTypes = {
  users: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};
export default UsersPage;
