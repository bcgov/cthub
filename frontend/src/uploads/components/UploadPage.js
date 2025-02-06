import PropTypes from "prop-types";
import React from "react";
import {
  Box,
  Button,
  MenuItem,
  Select,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
} from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import DownloadIcon from "@mui/icons-material/Download";
import FileDropArea from "./FileDropArea";
import Loading from "../../app/components/Loading";
import FileRequirements from "./FileRequirements";

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
    totalIssueCount,
    clearErrors,
    failedFiles,
  } = props;

  const selectionList = datasetList.map((obj, index) => (
    <MenuItem key={index} value={obj.name}>
      {obj.name}
    </MenuItem>
  ));

  const noIssues = (totalIssueCount) => {
    return (
      Object.keys(totalIssueCount).length === 0 &&
      totalIssueCount.constructor === Object
    );
  };

  return (
    <>
      <Box p={3}>
        <h2>Upload Program Data</h2>
        {noIssues && alertElement}
        <div id="dataset-select">
          <span>
            <h3>Select Program &nbsp; &nbsp;</h3>
          </span>
          <Select
            value={datasetSelected}
            style={{ minWidth: 220, backgroundColor: "white" }}
            onChange={(e) => {
              setDatasetSelected(e.target.value);
              setAlert(false);
            }}
          >
            {selectionList}
          </Select>
          {datasetSelected && (
            <Button
              className="button-dark-blue button-lowercase"
              type="button"
              variant="contained"
              onClick={downloadSpreadsheet}
              sx={{ ml: 2 }}
            >
              <DownloadIcon />
              Download Dataset Template
            </Button>
          )}
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
                disabled={datasetSelected ? false : true}
                value="add"
                control={<Radio />}
                label="Add to existing data (default)"
              />
              <FormControlLabel
                disabled={datasetSelected ? false : true}
                value="replace"
                control={<Radio />}
                label="Replace existing data (data cannot be restored, proceed only if you are certain that the new file contains all required data)."
              />
            </RadioGroup>
          </FormControl>
        </div>
        <div>
          <FileDropArea
            disabled={uploadFiles.length != 0 || !datasetSelected}
            setAlert={setAlert}
            setUploadFiles={setUploadFiles}
            uploadFiles={uploadFiles}
            totalIssueCount={totalIssueCount}
            clearErrors={clearErrors}
            failedFiles={failedFiles}
          />
        </div>
        <Box pt={3} rb={2}>
          <FileRequirements datasetSelected={datasetSelected} />
        </Box>
        <Box
          pt={2}
          className="upload-bar"
          alignItems="center"
          padding={2}
          display="flex"
          justifyContent="flex-end"
        >
          {loading ? (
            <Loading color="button-dark-blue" />
          ) : (
            <Button
              disabled={uploadFiles.length === 0 || !datasetSelected}
              className="button-dark-blue button-lowercase"
              onClick={() => doUpload(true)}
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
  replaceData: PropTypes.oneOfType([PropTypes.string, PropTypes.bool])
    .isRequired,
  handleRadioChange: PropTypes.func.isRequired,
  downloadSpreadsheet: PropTypes.func.isRequired,
  setAlert: PropTypes.func.isRequired,
};
export default UploadPage;
