import React from 'react';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDrop from './FileDrop';
import getFileSize from '../../app/utilities/getFileSize';

const FileDropArea = (props) => {
  const {
    uploadFiles,
    setUploadFiles,
    doUpload,
  } = props;

  const removeFile = (removedFile) => {
    const found = uploadFiles.findIndex((file) => (file === removedFile));
    uploadFiles.splice(found, 1);
    setUploadFiles([...uploadFiles]);
  };

  return (
    <div className="bordered">
      <div className="panel panel-default">
        <div className="content p-3">

          <FileDrop setFiles={setUploadFiles} maxFiles={1} allowedFileTypes="'application/vnd.ms-excel'" />
        </div>
        <div className="form-group mt-4 row">
          <div className="col-12 text-blue">  
            <strong>Limit of ??? files</strong>
          </div>
        </div>
        {uploadFiles.length > 0 && (
        <div className="files px-3">
          <div className="row pb-1">
            <div className="col-8 header"><label htmlFor="filename">Filename</label></div>
            <div className="col-3 size header"><label htmlFor="filesize">Size</label></div>
            <div className="col-1 actions header" />
          </div>
          {uploadFiles.map((file) => (
            <div className="row py-1" key={file.name}>
              <div className="col-8">{file.name}</div>
              <div className="col-3 size">{getFileSize(file.size)}</div>
              <div className="col-1 actions">
                <button
                  className="delete"
                  onClick={() => {
                    removeFile(file);
                  }}
                  type="button"
                >
                  <DeleteIcon />
                </button>
              </div>
            </div>
          ))}
        </div>
        )}
      </div>
    </div>
  );
};
export default FileDropArea;
