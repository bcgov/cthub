import React, { useState } from 'react';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import FileDropArea from './FileDropArea';

const UploadPage = (props) => {
  const {
    datasetList, data, uploadFiles, setUploadFiles, doUpload,
  } = props;

  const selectionList = datasetList.map((obj) => (
    <option key={obj} value={obj}>{obj}</option>
  ));
  return (
    <>
      <div className="row">
        <div className="col-12 mr-2">
          dataset to upload
          <Select className="ml-2">
            {selectionList}
          </Select>
        </div>
        <div>
          <FileDropArea
            setUploadFiles={setUploadFiles}
            uploadFiles={uploadFiles}
            doUpload={doUpload}
          />
        </div>

      </div>
      <div>
        <Button
        // disabled={uploadFiles.length === 0}
          className="button primary"
          onClick={() => doUpload()}
          type="button"
        >
          <FileUploadIcon />
          {' '}
          Upload
        </Button>
      </div>
    </>
  );
};
export default UploadPage;
