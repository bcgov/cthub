import PropTypes from 'prop-types';
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import FileUploadIcon from '@mui/icons-material/FileUpload';

const FileDrop = (props) => {
  const {
    setErrorMessage, setFiles, maxFiles, allowedFileTypes,
  } = props;
  const [dropMessage, setDropMessage] = useState('');
  const onDrop = useCallback((acceptedFiles) => {
    console.log(acceptedFiles)
    if (acceptedFiles.length > maxFiles) {
      setDropMessage(`Please select only ${maxFiles} file${maxFiles !== 1 ? 's' : ''}.`);
    } else {
      setDropMessage('');
      setErrorMessage('');
      setFiles(acceptedFiles);
    }
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: allowedFileTypes });
  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      <div className="file-upload">
        <FileUploadIcon/>
        <br />
        Drag and Drop files here or
        {' '}
        <br />
        <button className="link text-center" type="button">browse to select a file from your machine to upload.</button>
        {dropMessage && (
          <div id="danger-text">{dropMessage}</div>
        )}
      </div>
    </div>
  );
};

FileDrop.defaultProps = {
  allowedFileTypes: null,
  maxFiles: 5,
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
