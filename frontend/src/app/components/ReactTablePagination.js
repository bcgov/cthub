import PropTypes from "prop-types";
import React from "react";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import { makeStyles } from "@mui/styles";

import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";

const useStyles = makeStyles(() => ({
  pagination: {
    flexShrink: 0,
    "& .MuiSelect-select": {
      paddingBottom: "0.5rem",
      paddingTop: "0.5rem",
    },
  },
}));

const ReactTablePagination = (props) => {
  const classes = useStyles();
  const { count, onPageChange, page, rowsPerPage } = props;

  const pagesCount = Math.ceil(count / rowsPerPage);

  return (
    <div className={classes.pagination}>
      {pagesCount > 0 && (
        <>
          <IconButton
            aria-label="Previous Page"
            disabled={page === 0}
            onClick={(event) => {
              onPageChange(event, page - 1);
            }}
          >
            <KeyboardArrowLeft />
          </IconButton>

          <Select
            aria-label="Go to page"
            onChange={(event) => {
              const { value } = event.target;

              onPageChange(event, value);
            }}
            value={page}
          >
            {Array.from(Array(pagesCount).keys()).map((value) => (
              <MenuItem key={value} value={value}>
                {value + 1}
              </MenuItem>
            ))}
          </Select>

          <IconButton
            aria-label="Next Page"
            disabled={page >= pagesCount - 1}
            onClick={(event) => {
              onPageChange(event, page + 1);
            }}
          >
            <KeyboardArrowRight />
          </IconButton>
        </>
      )}
    </div>
  );
};

ReactTablePagination.propTypes = {
  count: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  page: PropTypes.number.isRequired,
  rowsPerPage: PropTypes.number.isRequired,
};

export default ReactTablePagination;
