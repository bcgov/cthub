import PropTypes from "prop-types";
import React from "react";
import { Box, Paper, Typography, AccordionSummary, AccordionDetails, Accordion } from "@mui/material";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import UploadIssuesDetail from "./UploadIssuesDetail";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const UploadIssues = (props) => {
  const { issues } = props;
  const errors = issues.filter(issue => issue.Severity === 'Error');
  const warnings = issues.filter(issue => issue.Severity === 'Warning');
 const getTotalRows = (severity) => {
    return issues.reduce((totalRows, issue) => {
      if (issue.Severity === severity) {
        return totalRows + issue.Rows.length;
      }
      return totalRows;
    }, 0);
  };
 const errorMsg = "Must fix before uploading"
 const warningMsg = "Can upload without fixing"
 return (
<Paper>
  <Box sx={{ p: 2 }}>

  <h2 style={{ marginBottom: '16px' }}>
    <InfoOutlinedIcon className="error" sx={{ marginLeft: 1, marginRight: 1 }} />
     Your file upload results
  </h2>
  <Box sx={{ ml: '2rem', mb: '1rem' }}>
    Your file has been processed and contains the following errors and warnings. Please review them below:
  </Box>
    {errors &&
  <Box ml={2} mt={2} >
    <span className="error">
      <strong>
        {getTotalRows('Error')} Errors  &nbsp;
      </strong>
    </span>
    - {errorMsg}
  </Box>
    }
  {warnings && 
    <Box ml={2} mt={2}>
      <span className="warning">
      <strong>
        {getTotalRows('Warning')} Warnings  &nbsp;
      </strong>
      </span>
      - {warningMsg}
    </Box>
  }
   <Accordion>
    <AccordionSummary
      aria-controls="panel1-content"
      id="panel1-header"
      sx={{
        marginLeft: '85%',
        paddingRight: '24px',
      }}
    >
      <Typography className="showMore" sx={{fontWeight:"bold"}}>Show more</Typography>
      <ExpandMoreIcon />
      </AccordionSummary>
        <AccordionDetails>
          {errors &&
            <UploadIssuesDetail type={"errors"} issues={errors} getTotalRows={getTotalRows} msg={errorMsg}/>
          }
          {warnings &&
            <UploadIssuesDetail type={"warnings"} issues={warnings} getTotalRows={getTotalRows} msg={warningMsg} />
          }
        </AccordionDetails>
      </Accordion>


  </Box>
</Paper>
 )
};

UploadIssues.defaultProps = {

};

UploadIssues.propTypes = {

};

export default UploadIssues;
