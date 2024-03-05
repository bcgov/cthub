import PropTypes from 'prop-types';
import React from 'react';
import {
  Box, Button, MenuItem, Select, Radio, RadioGroup, FormControlLabel, FormControl,
} from '@mui/material';
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
    replaceData,
    handleRadioChange,
    downloadSpreadsheet,
  } = props;
  const selectionList = datasetList.map((obj, index) => (
    <MenuItem key={index} value={obj.name}>
      {obj.name}
    </MenuItem>
  ));
  return (
    <>
      <Box p={3}>
        <h2>Upload Program Data</h2>
        <div id="dataset-select">
          <span>
            <h3>
              Select Program &nbsp; &nbsp;
            </h3>
          </span>
          <Select
            value={datasetSelected}
            style={{ minWidth: 220, backgroundColor: 'white'}}
            onChange={(e) => { setDatasetSelected(e.target.value); }}
          >
            {selectionList}
          </Select>
          <Button className="text-button" onClick={downloadSpreadsheet}>Download Spreadsheet</Button>

        </div>
        <div id="replace-data-select">
          <FormControl component="fieldset">
            <RadioGroup
              aria-label="Replace or add to existing data"
              value={replaceData}
              name="radio-buttons-group"
              onChange={handleRadioChange}
            >
              <FormControlLabel
                value
                control={(
                  <Radio />
)}
                label="Replace existing data"
              />
              <FormControlLabel
                value={false}
                control={<Radio />}
                label="Add to existing data"
              />
            </RadioGroup>
          </FormControl>
        </div>
        <div>
          <FileDropArea
            setUploadFiles={setUploadFiles}
            uploadFiles={uploadFiles}
          />
        </div>
        <Box pt={2} className="upload-bar" alignItems="center" padding={2} display="flex" justifyContent="flex-end">
          <Button
            disabled={uploadFiles.length === 0 || !datasetSelected}
            className="button-dark-blue"
            onClick={() => doUpload()}
            type="button"
            variant="contained"
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
  datasetList: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  uploadFiles: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  setUploadFiles: PropTypes.func.isRequired,
  doUpload: PropTypes.func.isRequired,
  setDatasetSelected: PropTypes.func.isRequired,
  replaceData: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.bool,
  ]).isRequired,
  handleRadioChange: PropTypes.func.isRequired,
};
export default UploadPage;
