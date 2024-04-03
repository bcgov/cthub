import PropTypes from 'prop-types';
import React from 'react';
import {
  Box, Button, MenuItem, Select, Radio, RadioGroup, FormControlLabel, FormControl,
} from '@mui/material';
import UploadIcon from '@mui/icons-material/Upload';
import FileDropArea from './FileDropArea';
import Loading from '../../app/components/Loading';

const UploadPage = (props) => {
  const {
    alertElement,
    datasetList,
    datasetSelected,
    doUpload,
    setDatasetSelected,
    setUploadFiles,
    uploadFiles,
    replaceData,
    handleRadioChange,
    downloadSpreadsheet,
    setAlert,
    loading,
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
        {alertElement}
        <div id="dataset-select">
          <span>
            <h3>
              Select Program &nbsp; &nbsp;
            </h3>
          </span>
          <Select
            value={datasetSelected}
            style={{ minWidth: 220, backgroundColor: 'white'}}
            onChange={(e) => { setDatasetSelected(e.target.value); setAlert(false); }}
          >
            {selectionList}
          </Select>
          {datasetSelected && <Button className="text-button" onClick={downloadSpreadsheet}>Download Excel File (program data upload template)</Button>}

        </div>
        <div id="replace-data-select">
          <FormControl component="fieldset">
            <RadioGroup
              aria-label="Replace or add to existing data"
              value={replaceData ? "replace" : "add"}
              name="radio-buttons-group"
              onChange={handleRadioChange}
              defaultValue="add"
            >
              <FormControlLabel
                disabled={datasetSelected ? false: true}
                value="add"
                control={<Radio />}
                label="Add to existing data (default)"
              />
              <FormControlLabel
                disabled={datasetSelected ? false: true}
                value="replace"
                control={<Radio />}
                label="Replace existing data (data cannot be restored, proceed only if you are certain that the new file contains all required data)."
              />
            </RadioGroup>
          </FormControl>
        </div>
        <div>
          <FileDropArea
            disabled={datasetSelected ? false: true}
            setAlert={setAlert}
            setUploadFiles={setUploadFiles}
            uploadFiles={uploadFiles}
          />
        </div>
        <Box pt={2} className="upload-bar" alignItems="center" padding={2} display="flex" justifyContent="flex-end">
          {loading ? (
            <Loading color="button-dark-blue" />
          ) : (
            <Button
              disabled={uploadFiles.length === 0 || !datasetSelected}
              className="button-dark-blue button-lowercase"
              onClick={() => doUpload()}
              type="button"
              variant="contained"
            >
              <UploadIcon />
              Upload
            </Button>
          )}
        </Box>
      </Box>
    </>
  );
};
UploadPage.defaultProps = {
  datasetSelected: {},
};

UploadPage.propTypes = {
  alertElement: PropTypes.element,
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
  downloadSpreadsheet: PropTypes.func.isRequired,
  setAlert: PropTypes.func.isRequired,
};
export default UploadPage;
