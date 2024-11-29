import React, { useState } from "react";
import {
  Box,
  Typography,
  AccordionSummary,
  AccordionDetails,
  Accordion,
  Button,
} from "@mui/material";
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import UploadIssuesDetail from "./UploadIssuesDetail";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const UploadIssues = ({
  confirmUpload,
  groupedCriticalErrors,
  groupedErrors,
  groupedWarnings,
  totalIssueCount,
  clearErrors,
  setUploadFiles
}) => {
  const [showAllIssues, setShowAllIssues] = useState(false);

  const toggleShowAllIssues = () => {
    setShowAllIssues(!showAllIssues);
  };

  const criticalMsg = "Must fix before file can be processed";
  const errorMsg = "Must fix before uploading";
  const warningMsg = "Can upload without fixing";
  const renderUploadFailed = () => {
      const missingHeadersError = groupedCriticalErrors?.Headers?.["Missing Headers"];
      let missingHeadersMsg = '';
      if (missingHeadersError) {
        const missingColumns = missingHeadersError.Rows;
        const columnsText = missingColumns.length === 1
          ? `column "${missingColumns[0]} is "`
          : `columns "${missingColumns.join(', ')}" are `;
      
        missingHeadersMsg = `Your file has been processed and the ${columnsText} not found in the dataset. 
          Please ensure that your dataset matches the provided template, and that all required columns are present. 
          You can download the template for reference. Once corrected, you can upload your file again.`;
      }
      const missingWorksheetError = groupedCriticalErrors?.Spreadsheet?.["Missing Worksheet"];
      let missingWorksheetMsg = '';
      if (missingWorksheetError) {
        const sheetName = groupedCriticalErrors.Spreadsheet['Missing Worksheet'].Rows[0]
        missingWorksheetMsg = missingWorksheetError ? 
        `File Upload Failed - The sheet name doesn't match the required “${sheetName}”.
        Please rename the sheet to the required “${sheetName}” before the next upload.` : '';
      }
      const errorMsg = missingHeadersMsg || missingWorksheetMsg;  
    return (
      <Box ml={4} mt={2}>
        {errorMsg}
      </Box>
    )
  }
      

  const errorHeading = () => {
    const missingHeadersError = groupedCriticalErrors?.Headers?.['Missing Headers']?.ExpectedType;
    const missingWorksheetError = groupedCriticalErrors?.Spreadsheet?.['Missing Worksheet']?.ExpectedType;
    return missingHeadersError || missingWorksheetError;
  }
  

  return (
    <>
      <Box sx={{ p: 2, mb: 2 }}>
        <h2 style={{ marginBottom: "16px" }}>
          <ErrorOutlineIcon
            className="error"
            sx={{ marginLeft: 1, marginRight: 1 }}
          />
         {totalIssueCount.criticalErrors >= 1 ? `File upload failed - ${errorHeading()}`: 'Your file upload results'}
        </h2>
        {totalIssueCount.criticalErrors >= 1 && (
          renderUploadFailed()
        )}
        {totalIssueCount.criticalErrors == 0 &&
          <Box sx={{ ml: "2rem", mb: "1rem" }}>
            Your file has been processed and contains the following errors and warnings. Please review them below
          </Box>
        }
        {totalIssueCount.errors >= 1 && (
          <Box ml={2} mt={2}>
            <span className="error">
              <strong>{totalIssueCount.errors} Errors &nbsp;</strong>
            </span>
            - {errorMsg}
          </Box>
        )}
        {totalIssueCount.warnings >= 1 && (
          <Box ml={2} mt={2}>
            <span className="warning">
              <strong>{totalIssueCount.warnings} Warnings &nbsp;</strong>
            </span>
            - {warningMsg}
          </Box>
        )}
        {totalIssueCount.criticalErrors == 0 && (
          <>
        <Accordion elevation={0} sx={{ "&:before": { height: "0px" } }}>
          <AccordionSummary
            aria-controls="panel1-content"
            id="panel1-header"
            sx={{
              marginLeft: "85%",
              paddingRight: "24px",
            }}
            onClick={toggleShowAllIssues}
          >
            <Typography className="showMore" sx={{ fontWeight: "bold" }}>
              {showAllIssues ? "Show less" : "Show more"}
            </Typography>
            <ExpandMoreIcon />
          </AccordionSummary>
          <AccordionDetails>
          {totalIssueCount.criticalErrors >= 1 && (
              <UploadIssuesDetail
                type="critical"
                issues={groupedCriticalErrors}
                totalIssueCount={totalIssueCount.criticalErrors}
                msg={criticalMsg}
              />
            )}
            {totalIssueCount.errors >= 1 && (
              <UploadIssuesDetail
                type="error"
                issues={groupedErrors}
                totalIssueCount={totalIssueCount.errors}
                msg={errorMsg}
              />
            )}
            {totalIssueCount.warnings >= 1 && (
              <UploadIssuesDetail
                type="warning"
                issues={groupedWarnings}
                totalIssueCount={totalIssueCount.warnings}
                msg={warningMsg}
              />
            )}
          </AccordionDetails>
        </Accordion>
        </>
        )}
        {
          totalIssueCount.warnings >= 1 && totalIssueCount.errors === 0 && (
          <Box>
            <h3>Do you want to upload the file regardless of the warnings?</h3>
            <Box mt={3}>
              <Button
                className="cancel-button"
                onClick={() => {
                  clearErrors()
                  setUploadFiles([])
                }}
              >
                Cancel
              </Button>
              <Button
                variant="contained"
                className="confirm-button"
                onClick={() => {
                  confirmUpload();
                }}
              >
                Upload File
              </Button>
            </Box>
          </Box>
        )}
      </Box>
    </>
  );
};

export default UploadIssues;
