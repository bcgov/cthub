import React from "react";
import PropTypes from "prop-types";
import {
  Box,
  Button,
  Grid,
  TextField,
  Checkbox,
  Tooltip,
  IconButton,
} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import SaveIcon from "@mui/icons-material/Save";

const UsersPage = (props) => {
  const {
    currentUser,
    users,
    handleAddNewUser,
    setNewUser,
    handleCheckboxChange,
    handleSubmitUserUpdates,
    newUser,
    setMessage,
    handleXClick,
    saveButtonEnabled,
  } = props;

  const userRow = (user) => {
    const disableAdmin = currentUser === user.idir;
    return (
      <Grid container key={user.idir} alignItems="center">
        <Grid item className="permissions">
          <Checkbox
            className="checkbox"
            name={user.idir}
            id="uploader"
            color="default"
            checked={user.user_permissions.uploader || false}
            onChange={(event) => {
              handleCheckboxChange(event);
            }}
          />
          <Tooltip
            disableHoverListener={!disableAdmin}
            title="You cannot remove your own admin permission"
          >
            <span>
              <Checkbox
                className="checkbox"
                name={user.idir}
                id="admin"
                color="default"
                disabled={disableAdmin}
                checked={user.user_permissions.admin || false}
                onChange={(event) => {
                  handleCheckboxChange(event);
                }}
              />
            </span>
          </Tooltip>
        </Grid>
        <Grid item md={2} paddingLeft={2}>
          <span>{user.idir}</span>
        </Grid>
        <Grid item>
          <Tooltip
            disableHoverListener={!disableAdmin}
            title="You cannot delete yourself."
          >
            <span>
              <IconButton
                padding={0}
                disabled={disableAdmin}
                onClick={() => {
                  handleXClick(user.idir);
                }}
              >
                <ClearIcon
                  padding={0}
                  sx={{ color: disableAdmin ? "grey" : "red" }}
                />
              </IconButton>
            </span>
          </Tooltip>
        </Grid>
      </Grid>
    );
  };

  return (
    <>
      <Box p={3}>
        <div>
          <h2>Admin</h2>
        </div>
        <Grid container>
          <Box
            display="flex"
            md={6}
            flexDirection="row"
            className="add-user-box"
            alignItems="center"
            padding={2}
            justifyContent="space-evenly"
          >
            <Grid
              container
              alignItems="center"
              justifyContent="space-around"
              spacing={2}
            >
              <Grid item>
                <h3>IDIR Username</h3>
              </Grid>
              <Grid item>
                <TextField
                  value={newUser}
                  className="user-input"
                  type="text"
                  onChange={(event) => {
                    setNewUser(event.target.value);
                    setMessage("");
                  }}
                />
              </Grid>
              <Grid item>
                <Tooltip
                  disableHoverListener={!!newUser}
                  title="Please type in the IDIR you would like to add."
                >
                  <span>
                    <Button
                      disabled={!newUser}
                      variant="contained"
                      className="button-dark-blue"
                      onClick={handleAddNewUser}
                    >
                      Add User
                    </Button>
                  </span>
                </Tooltip>
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid container display="flex" flexDirection="column">
          <Box
            className="permissions"
            justifyContent="space-around"
            display="flex"
            flexDirection="row"
            paddingTop={1}
          >
            <Box>
              <h4>Upload </h4>
            </Box>
            <Box>
              <h4>Admin</h4>
            </Box>
          </Box>
          {users.map((user) => userRow(user))}
          <Box
            className="permissions"
            justifyContent="space-around"
            display="flex"
            paddingTop={3}
            paddingBottom={3}
          >
            <Button
              variant="contained"
              className="button-dark-blue"
              startIcon={<SaveIcon />}
              onClick={handleSubmitUserUpdates}
              disabled={!saveButtonEnabled}
            >
              Save
            </Button>
          </Box>
        </Grid>
      </Box>
    </>
  );
};
UsersPage.defaultProps = {
  newUser: "",
};

UsersPage.propTypes = {
  users: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  handleAddNewUser: PropTypes.func.isRequired,
  setNewUser: PropTypes.func.isRequired,
  handleCheckboxChange: PropTypes.func.isRequired,
  handleSubmitUserUpdates: PropTypes.func.isRequired,
  currentUser: PropTypes.string.isRequired,
  newUser: PropTypes.string,
  setMessage: PropTypes.func.isRequired,
  handleXClick: PropTypes.func.isRequired,
};
export default UsersPage;
