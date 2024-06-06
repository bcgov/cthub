import PropTypes from "prop-types";
import React, { useCallback, useState } from "react";
import { Box, Button } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import { useDropzone } from "react-dropzone";

const FileDrop = (props) => {
  const { disabled, setFiles, setAlert } = props;
  const [dropMessage, setDropMessage] = useState("");
  const onDrop = useCallback((files) => {
    setAlert(false);
    setDropMessage("");
    setFiles(files);
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });
  const uploadBoxClassNames = disabled ? "file-upload disabled" : "file-upload";
  return (
    <div {...getRootProps()}>
      <input disabled={disabled} {...getInputProps()} />
      <div className={uploadBoxClassNames}>
        <UploadIcon />
        <br />
        Drag and Drop files here or <br />
        <Box p={2}>
          <Button className="text-button">
            browse to select a file from your machine to upload.
          </Button>
        </Box>
        {dropMessage && <div>{dropMessage}</div>}
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
  setAlert: PropTypes.func.isRequired,
};

export default FileDrop;
