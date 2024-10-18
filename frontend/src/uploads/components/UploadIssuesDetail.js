import PropTypes from "prop-types";
import React, { useState } from "react";
import { Box, Button } from "@mui/material";
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const UploadIssuesDetail = ({ type, issues, totalIssueCount, msg }) => {
  const [showAllRowsMap, setShowAllRowsMap] = useState({}); // State to toggle showing all rows for each issue
  const errorTypes = ['critical', 'error']
  const classname = errorTypes.includes(type) ? "error" : "warning";
  const toggleShowAllRows = (column, errorType) => {
    const key = `${column}_${errorType}`;
    setShowAllRowsMap((prevState) => ({
      ...prevState,
      [key]: !prevState[key],
    }));
  };

  return (
    <Box
      p={2}
      sx={{
        border: errorTypes.includes(type) ? "1px solid #ce3e39" : "1px solid #fcba19",
        mb: "1rem",
      }}
    >
      <ErrorOutlineIcon
        className={classname}
        sx={{ marginLeft: 1, marginRight: 1 }}
      />
      <span className={classname}>
        <strong>
          {totalIssueCount} {type === 'critical' ? 'Critical Errors' : type === 'error' ? 'Errors' : 'Warnings'}&nbsp;
        </strong>
      </span>
      ({msg})
      {Object.keys(issues).map((column) => (
        <Box key={column} sx={{ marginTop: 2 }}>
          <strong>Column: {column}</strong>
          {Object.keys(issues[column]).map((errorType, index) => (
            <div key={index} style={{ marginTop: "0.5rem" }}>
              <div>
                {(Object.keys(issues[column]).length > 1 ? `(${index + 1}) ` : '')}
                {type.charAt(0).toUpperCase() + type.slice(1)} {type === `critical` ? `Error` : `Name:`} <b>{errorType}</b>
                </div>
              <div>
                Expected value:{" "}
                <b>
                {issues[column][errorType].ExpectedType ||
                  issues[column][errorType].ExpectedFormat}
                </b>
              </div>
              <div>
              {column === 'Headers' ? `Missing Headers: ` : column === 'Spreadsheet' ? 'Missing Spreadsheet: ' : `Rows with ${type}: `}
                <b>
                  {issues[column][errorType].Rows.slice(
                    0,
                    showAllRowsMap[`${column}_${errorType}`] ? undefined : 15,
                  ).join(", ")}
                  {issues[column][errorType].Rows.length > 15 &&
                    !showAllRowsMap[`${column}_${errorType}`] &&
                    "..."}
                </b>
              </div>
              {issues[column][errorType].Rows.length > 15 && (
                <Button
                  variant="text"
                  onClick={() => toggleShowAllRows(column, errorType)}
                >
                  {showAllRowsMap[`${column}_${errorType}`]
                    ? "Show less"
                    : "Show more"}{" "}
                  <ExpandMoreIcon />
                </Button>
              )}
            </div>
          ))}
        </Box>
      ))}
    </Box>
  );
};

UploadIssuesDetail.propTypes = {
  type: PropTypes.string.isRequired,
  issues: PropTypes.object.isRequired,
  totalIssueCount: PropTypes.number.isRequired,
  msg: PropTypes.string.isRequired,
};

export default UploadIssuesDetail;
