import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import {
  useAsyncDebounce,
  useFilters,
  usePagination,
  useSortBy,
  useTable,
} from 'react-table';

// material-ui core components
import CircularProgress from '@material-ui/core/CircularProgress';
import IconButton from '@material-ui/core/IconButton';
import InputAdornment from '@material-ui/core/InputAdornment';
import Popover from '@material-ui/core/Popover';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import makeStyles from '@material-ui/core/styles/makeStyles';

// material-ui icons
import FilterListIcon from '@material-ui/icons/FilterList';
import MoreVert from '@material-ui/icons/MoreVert';

// components
import ReactTablePagination from './ReactTablePagination';

const useStyles = makeStyles(() => ({
  moreOptions: {
    alignItems: 'center',
    display: 'inline-flex',
    height: '100%',
    position: 'absolute',
    right: 0,
    top: 0,
    zIndex: '999',
    '&.active': {
      opacity: '1 !important',
    },
  },
  cellMoreOptions: {
    '& $moreOptions': {
      opacity: 0,
    },
    '&:hover $moreOptions': {
      opacity: 0.5,
    },
  },
  popoverContainer: {
    padding: '0.75rem',
  },
  popoverInputFilter: {
    '& input': {
      padding: '0.75rem',
    },
  },
  reactTable: {
    position: 'relative',
    '& caption': {
      bottom: 0,
      left: 0,
      padding: 0,
      position: 'absolute',
      right: 0,
      top: 0,
      zIndex: 999,
    },
    '& caption > div': {
      alignItems: 'center',
      backgroundColor: 'rgba(255, 255, 255, 0.7)',
      display: 'flex',
      height: '100%',
      justifyContent: 'center',
      width: '100%',
    },
  },
}));

const ReactTable = (props) => {
  const classes = useStyles();

  const {
    columns,
    data,
    defaultSortBy,
    filterable,
    loading,
    onFetchData,
    pageCount: controlledPageCount,
    size,
    sortable,
    totalRowsCount,
  } = props;

  const [anchorEl, setAnchorEl] = useState(null);
  const [filterColumn, setFilterColumn] = useState(null);
  const [filters, setFilters] = useState([]);

  const {
    getTableBodyProps,
    getTableProps,
    gotoPage,
    headerGroups,
    page,
    prepareRow,
    setPageSize,
    state: {
      pageIndex,
      pageSize,
      sortBy,
    },
  } = useTable({
    columns,
    data,
    disableSortBy: !sortable,
    disableSortRemove: true,
    initialState: {
      filters: [],
      pageIndex: 0,
      sortBy: defaultSortBy,
    },
    manualFilters: true,
    manualPagination: true,
    manualSortBy: true,
    pageCount: controlledPageCount,
  }, useFilters, useSortBy, usePagination);

  const handleFilterColumn = useAsyncDebounce((event) => {
    const { value } = event.target;
    let { filterBy } = filterColumn;

    if (!filterBy) {
      filterBy = filterColumn.id;
    }

    const foundIndex = filters.findIndex((filter) => (filter.id === filterBy));

    if (foundIndex >= 0) {
      filters[foundIndex].value = value;
    } else {
      filters.push({
        id: filterBy,
        value,
      });
    }

    setFilters([...filters]);
  }, 500);

  const handleOpenMoreOptions = (event) => {
    event.stopPropagation();
    event.currentTarget.parentNode.classList.add('active');

    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    anchorEl.parentNode.classList.remove('active');

    setAnchorEl(null);
  };

  useEffect(() => {
    onFetchData({
      columns, pageIndex, pageSize, sortBy, filters,
    });
  }, [onFetchData, pageIndex, pageSize, sortBy, filters]);

  const open = Boolean(anchorEl);

  return (
    <>
      <TableContainer>
        <Table className={classes.reactTable} {...getTableProps()} stickyHeader size={size}>
          {loading && (
            <caption>
              <div>
                <CircularProgress color="inherit" />
              </div>
            </caption>
          )}
          <TableHead>
            {headerGroups.map((headerGroup) => (
              <TableRow {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <TableCell
                    {...column.getHeaderProps(column.getSortByToggleProps())}
                    align={column.headerAlign ? column.headerAlign : 'center'}
                    className={classes.cellMoreOptions}
                  >
                    <TableSortLabel
                      active={sortable && column.sortable !== false && column.isSorted}
                      direction={column.isSortedDesc ? 'desc' : 'asc'}
                      hideSortIcon={!sortable || column.sortable === false}
                    >
                      {column.render('Header')}
                    </TableSortLabel>

                    {filterable && column.filterable !== false && (
                      <span className={classes.moreOptions}>
                        <Tooltip title="More options" arrow placement="top">
                          <IconButton
                            onClick={(event) => {
                              handleOpenMoreOptions(event);
                              setFilterColumn(column);
                            }}
                            size="small"
                            type="button"
                          >
                            <MoreVert />
                          </IconButton>
                        </Tooltip>
                      </span>
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableHead>

          <TableBody {...getTableBodyProps()}>
            {page && page.map((row) => {
              prepareRow(row);

              return (
                <TableRow {...row.getRowProps()}>
                  {row.cells.map((cell) => (
                    <TableCell
                      {...cell.getCellProps()}
                      align={cell.column.align ? cell.column.align : 'left'}
                      width={cell.column.width}
                    >
                      {cell.render('Cell')}
                    </TableCell>
                  ))}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        ActionsComponent={ReactTablePagination}
        component="div"
        count={totalRowsCount}
        page={pageIndex}
        onChangePage={(e, pageNumber) => {
          gotoPage(pageNumber);
        }}
        onChangeRowsPerPage={(event) => {
          setPageSize(Number(event.target.value));
          gotoPage(0);
        }}
        rowsPerPage={pageSize}
      />

      <Popover
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        open={open}
        onClose={handleClose}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <div className={classes.popoverContainer}>
          <TextField
            className={classes.popoverInputFilter}
            defaultValue={
              filterColumn && filters.find(
                (filter) => filter.id === filterColumn.filterBy || filter.id === filterColumn.id,
              ) ? filters.find((filter) => filter.id === filterColumn.filterBy || filter.id === filterColumn.id).value : ''
            }
            InputLabelProps={{
              shrink: true,
            }}
            InputProps={{
              endAdornment: (
                <InputAdornment>
                  <FilterListIcon />
                </InputAdornment>
              ),
            }}
            label={`Filter by ${filterColumn && filterColumn.Header}`}
            onChange={(event) => (handleFilterColumn(event))}
            placeholder={filterColumn && filterColumn.Header}
            type="text"
            variant="outlined"
          />
        </div>
      </Popover>
    </>
  );
};

ReactTable.defaultProps = {
  defaultSortBy: [],
  filterable: true,
  size: 'small',
  sortable: true,
};

ReactTable.propTypes = {
  columns: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  defaultSortBy: PropTypes.arrayOf(PropTypes.shape()),
  filterable: PropTypes.bool,
  loading: PropTypes.bool.isRequired,
  onFetchData: PropTypes.func.isRequired,
  pageCount: PropTypes.number.isRequired,
  size: PropTypes.string,
  sortable: PropTypes.bool,
  totalRowsCount: PropTypes.number.isRequired,
};

export default ReactTable;
