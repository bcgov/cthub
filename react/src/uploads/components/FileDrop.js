import PropTypes from 'prop-types';
import React, { useCallback, useState } from 'react';
import Box from '@material-ui/core/Box';
import Button from '@mui/material/Button';
import { useDropzone } from 'react-dropzone';

const FileDrop = (props) => {
  const {
    setFiles,
  } = props;
  const [dropMessage, setDropMessage] = useState('');
  const onDrop = useCallback((files) => {
    setDropMessage('');
    setFiles(files);
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });
  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      <div className="file-upload">
        {/* <FileUploadIcon/> */}
        <br />
        Drag and Drop files here or
        {' '}
        <br />
        <Box p={2}>
          <Button variant="outlined">browse to select a file from your machine to upload.</Button>
        </Box>
        {dropMessage && (
          <div>{dropMessage}</div>
        )}
      </div>
    </div>
  );
};

FileDrop.defaultProps = {
  allowedFileTypes: null,
  maxFiles: 1,
  setErrorMessage: () => {},
  setFiles: () => {},
};

FileDrop.propTypes = {
  setErrorMessage: PropTypes.func,
  setFiles: PropTypes.func,
  maxFiles: PropTypes.number,
  allowedFileTypes: PropTypes.string,
};

export default FileDrop;
