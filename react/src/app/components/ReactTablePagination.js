import PropTypes from 'prop-types';
import React from 'react';
import IconButton from '@material-ui/core/IconButton';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import makeStyles from '@material-ui/core/styles/makeStyles';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';

const useStyles = makeStyles((theme) => ({
  pagination: {
    flexShrink: 0,
    marginLeft: theme.spacing(2.5),
  },
}));

const ReactTablePagination = (props) => {
  const classes = useStyles();
  const {
    count,
    onChangePage,
    page,
    rowsPerPage,
  } = props;

  const pagesCount = Math.ceil(count / rowsPerPage);

  return (
    <div className={classes.pagination}>
      {pagesCount > 0 && (
        <>
          <IconButton
            aria-label="Previous Page"
            disabled={page === 0}
            onClick={(event) => {
              onChangePage(event, page - 1);
            }}
          >
            <KeyboardArrowLeft />
          </IconButton>

          <Select
            aria-label="Go to page"
            onChange={(event) => {
              const { value } = event.target;

              onChangePage(event, value);
            }}
            value={page}
          >
            {Array.from(Array(pagesCount).keys()).map((value) => (
              <MenuItem key={value} value={value}>{(value + 1)}</MenuItem>
            ))}
          </Select>

          <IconButton
            aria-label="Next Page"
            disabled={page >= pagesCount - 1}
            onClick={(event) => {
              onChangePage(event, page + 1);
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
  onChangePage: PropTypes.func.isRequired,
  page: PropTypes.number.isRequired,
  rowsPerPage: PropTypes.number.isRequired,
};

export default ReactTablePagination;
