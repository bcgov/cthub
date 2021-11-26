import React from 'react';
import PropTypes from 'prop-types';
import Box from '@material-ui/core/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDrop from './FileDrop';
import getFileSize from '../../app/utilities/getFileSize';

const FileDropArea = (props) => {
  const {
    setUploadFiles,
    uploadFiles,
  } = props;

  const removeFile = (removedFile) => {
    const found = uploadFiles.findIndex((file) => (file === removedFile));
    uploadFiles.splice(found, 1);
    setUploadFiles([...uploadFiles]);
  };

  function FormRow(file) {
    const { name, size } = file;
    return (
      <React.Fragment key={name} className="upload-row">
        <Grid item xs={7}>
          {name}
        </Grid>
        <Grid item xs={3} className="upload-row">
          {getFileSize(size)}
        </Grid>
        <Grid item xs={2} className="upload-row">

          <Button
            className="delete"
            onClick={() => {
              removeFile(file);
            }}
            type="button"
            id="trash-button"
          >
            <DeleteIcon />
          </Button>
        </Grid>
      </React.Fragment>
    );
  }
  return (
    <div className="bordered">
      <div>
        <div className="content">
          <Box p={3}>
            <FileDrop
              setFiles={setUploadFiles}
            />
          </Box>
        </div>
        {uploadFiles.length > 0 && (
        <Box className="upload-list" pt={3} rb={2}>
          <Grid container direction="row">
            <Grid item xs={7}>
              Filename
            </Grid>
            <Grid item xs={3}>
              Size
            </Grid>
            <Grid item xs={2} />
            {uploadFiles.map((file) => (
              FormRow(file)
            ))}
          </Grid>
        </Box>
        )}
      </div>
    </div>
  );
};
FileDropArea.propTypes = {
  setUploadFiles: PropTypes.func.isRequired,
  uploadFiles: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};
export default FileDropArea;
