import PropTypes from 'prop-types';
import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import UploadIcon from '@mui/icons-material/Upload';

import FileDropArea from './FileDropArea';

const UploadPage = (props) => {
  const {
    datasetList,
    datasetSelected,
    doUpload,
    setDatasetSelected,
    setUploadFiles,
    uploadFiles,
  } = props;
  const selectionList = datasetList.map((obj) => (
    <MenuItem key={obj} value={obj}>{obj}</MenuItem>
  ));
  return (
    <>
      <Box p={3}>
        <div id="dataset-select">
          <span>
            Dataset to Upload &nbsp; &nbsp;
          </span>
          <Select
            value={datasetSelected}
            style={{ minWidth: 220 }}
            onChange={(e) => { setDatasetSelected(e.target.value); }}
          >
            {selectionList}
          </Select>
        </div>
        <div>
          <FileDropArea
            setUploadFiles={setUploadFiles}
            uploadFiles={uploadFiles}
          />
        </div>
        <Box pt={2}>
          <Button
            disabled={uploadFiles.length === 0 || !datasetSelected}
            className="button primary"
            onClick={() => doUpload()}
            type="button"
            variant="outlined"
          >
            <UploadIcon />
            Upload
          </Button>
        </Box>
      </Box>
    </>
  );
};
UploadPage.defaultProps = {
  datasetSelected: {},
};

UploadPage.propTypes = {
  datasetSelected: PropTypes.string,
  datasetList: PropTypes.arrayOf(PropTypes.string).isRequired,
  uploadFiles: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  setUploadFiles: PropTypes.func.isRequired,
  doUpload: PropTypes.func.isRequired,
  setDatasetSelected: PropTypes.func.isRequired,
};
export default UploadPage;
