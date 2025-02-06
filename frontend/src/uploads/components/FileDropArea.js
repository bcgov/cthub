import React, { useState } from "react";
import PropTypes from "prop-types";
import { Box, Button, Grid, Tooltip } from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import FileDrop from "./FileDrop";
import getFileSize from "../../app/utilities/getFileSize";
import AlertDialog from "../../app/components/AlertDialog"

const FileDropArea = (props) => {
  const {
    disabled,
    setUploadFiles,
    uploadFiles,
    setAlert,
    totalIssueCount,
    clearErrors,
    failedFiles,
  } = props;

  const removeFile = (removedFile) => {
    const found = uploadFiles.findIndex((file) => file === removedFile);
    uploadFiles.splice(found, 1);
    setUploadFiles([...uploadFiles]);
  };

  const [fileToDelete, setFileToDelete] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);

  const handleDeleteConfirm = () => {

    removeFile(fileToDelete)

    clearErrors();
    setFileToDelete(null);

    setOpenDialog(false);
  };

  const handleDeleteCancel = () => {
    setFileToDelete(null);
    setOpenDialog(false);
  };

  const handleDeleteClick = (file) => {
    setFileToDelete(file);
    setOpenDialog(true);
  };

  function FormRow(file, success) {
    const { name, size } = file;
    const uploadRowClassname =
      totalIssueCount.criticalErrors >= 1
        ? "error"
        : success == false
          ? "error"
          : "upload-row";
    return (
      <>
        <AlertDialog
          open={openDialog}
          title={"Delete Your Dataset"}
          dialogue={"Are you sure you want to delete the dataset you just processed? Don't worry, you'll be able to upload a new one right after."} // Corrected prop name
          cancelText={"Cancel"}
          handleCancel={handleDeleteCancel}
          confirmText={"Delete"}
          handleConfirm={handleDeleteConfirm}
          confirmButtonStyle={{
            color: "red",
            border: "1px solid red",
            "&:hover": {
              backgroundColor: "#ffe6e6",
            },
          }}
        />
        <Grid container alignItems="center" key={name}>
          <Grid item xs={7} className={uploadRowClassname}>
            {name}
          </Grid>
          <Grid item xs={3} className={uploadRowClassname}>
            {getFileSize(size)}
          </Grid>
          <Grid item xs={2} className={uploadRowClassname}>
            {success == true && (
              <Button
                className="delete"
                onClick={() => {
                  handleDeleteClick()
                }}
                type="button"
                id="trash-button"
              >
                <ClearIcon padding={0} sx={{ color: "red" }} />
              </Button>
            )}
            {success == false && <>Failed Upload</>}
          </Grid>
        </Grid>
      </>
    );
  }
  return (
    <div>
      <div>
        <div className="content">
          <Box p={2}>
            <Tooltip
              disableHoverListener={!disabled}
              title={
                uploadFiles.length != 0
                  ? "To upload another dataset, please delete the current dataset\
                 by clicking the delete icon next to the file name and size."
                  : "Select a program to unlock this drag-and-drop area for dataset upload"
              }
            >
              <span>
                <FileDrop
                  disabled={disabled}
                  setAlert={setAlert}
                  setFiles={setUploadFiles}
                  clearErrors={clearErrors}
                />
              </span>
            </Tooltip>
          </Box>
        </div>
        {(uploadFiles.length > 0 || failedFiles.length > 0) && (
          <Box className="upload-list" pt={3} rb={2}>
            <Grid container direction="row">
              <Grid item xs={7}>
                <h3>Filename</h3>
              </Grid>
              <Grid item xs={3}>
                <h3>Size</h3>
              </Grid>
              <Grid item xs={2} />
              {failedFiles.map((failed, index) => {
                return failed.map((file) => {
                  return FormRow(file, false);
                });
              })}
              {uploadFiles.map((file) => FormRow(file, true))}
            </Grid>
          </Box>
        )}
      </div>
    </div>
  );
};
FileDropArea.propTypes = {
  disabled: PropTypes.bool.isRequired,
  setUploadFiles: PropTypes.func.isRequired,
  uploadFiles: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  setAlert: PropTypes.func.isRequired,
};
export default FileDropArea;
