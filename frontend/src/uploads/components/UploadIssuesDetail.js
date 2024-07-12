import PropTypes from "prop-types";
import React, { useCallback, useState } from "react";
import { Box, Button } from "@mui/material";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

const UploadIssuesDetail = ( { type, issues, getTotalRows, msg }) => {
  const [showAllRows, setShowAllRows] = useState(false); //needs to be used to toggle show more rows
  const classname = type==="errors"? "error" : "warning"
  
   // Group issues by column
  const groupedIssues = issues.reduce((acc, issue) => {
    const { Column, ErrorType, ExpectedFormat, Severity, Rows } = issue;
    if (!acc[Column]) {
      acc[Column] = [];
    }
    acc[Column].push({ ErrorType, ExpectedFormat, Severity, Rows });
    return acc;
  }, {});


 return (
   <Box p={2} sx={{ border: type === "errors" ? "1px solid #ce3e39" : "1px solid #fcba19"}}>
      <InfoOutlinedIcon
        className={classname}
        sx={{ marginLeft: 1, marginRight: 1 }}
      />
      <span className={classname}>
      <strong>
        {getTotalRows('Warning')} {type}&nbsp;
      </strong>
      </span>
        ({msg})
      {Object.keys(groupedIssues).map((column) => (
         <Box key={column} sx={{ marginTop: 2 }}>
          <strong>Column: {column}</strong>
          {groupedIssues[column].map((issue, index) => (
             <div key={index}  >
              <div style={{ marginTop: '0.5rem' }}>Error Name {issue.ErrorType}</div>
              <div style={{ marginTop: '0.5rem' }}>Expected value: {issue.ExpectedFormat}</div>
              <div style={{ marginTop: '0.5rem' }}>Rows with this error: <b>{issue.Rows.join(', ')}</b></div>
{/* need to add logic to hide rows if there are more than 15 and use show more to display */}
            </div>
          ))}
          </Box>
      ))}
    </Box>
 )
};

UploadIssuesDetail.defaultProps = {

};

UploadIssuesDetail.propTypes = {

};

export default UploadIssuesDetail;
