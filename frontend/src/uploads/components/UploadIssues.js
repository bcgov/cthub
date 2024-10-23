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
}) => {
  const [showAllIssues, setShowAllIssues] = useState(false);

  const toggleShowAllIssues = () => {
    setShowAllIssues(!showAllIssues);
  };

  const criticalMsg = "Must fix before file can be processed";
  const errorMsg = "Must fix before uploading";
  const warningMsg = "Can upload without fixing";

  return (
    <>
      <Box sx={{ p: 2, mb: 2 }}>
        <h2 style={{ marginBottom: "16px" }}>
          <ErrorOutlineIcon
            className="error"
            sx={{ marginLeft: 1, marginRight: 1 }}
          />
          Your file upload results
        </h2>
        <Box sx={{ ml: "2rem", mb: "1rem" }}>
          {totalIssueCount.criticalErrors > 0 ? 'Your file cannot be processed because it contains critical errors. Please review them below.': 'Your file has been processed and contains the following errors and warnings. Please review them below'}
        </Box>
        {totalIssueCount.criticalErrors >= 1 && (
          <Box ml={2} mt={2}>
            <span className="error">
              <strong>{totalIssueCount.criticalErrors} Critical Errors &nbsp;</strong>
            </span>
            - {criticalMsg}
          </Box>
        )}
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
        {totalIssueCount.warnings >= 1 && totalIssueCount.errors === 0 && (
          <Box>
            <h3>Do you want to upload the file regardless of the warnings?</h3>
            <Box mt={3}>
              <Button
                className="cancel-button"
                onClick={() => {
                  console.log("cancel");
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
