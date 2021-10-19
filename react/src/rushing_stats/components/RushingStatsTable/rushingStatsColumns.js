import React from 'react';

const colWidth = 35;

const numericCell = (value, precision = 0) => {
  if (value < 0) {
    return <span className="text-danger">{value.toFixed(precision)}</span>;
  }

  return value.toFixed(precision);
};

const rushingStatsColumns = [{
  accessor: 'att_per_game',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: 'Att/G',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'att_total',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: 'Att',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'yds_total',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: 'Yds',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'yds_avg_per_att',
  Cell: (item) => (numericCell(item.value, 1)),
  align: 'right',
  Header: 'Avg',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'yds_per_game',
  Cell: (item) => (numericCell(item.value, 1)),
  align: 'right',
  Header: 'Yds/G',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'td_total',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: 'TD',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: (item) => (`${item.rush_max}${item.rush_max_td ? 'T' : ''}`),
  Cell: (item) => {
    const { row } = item;

    return (
      <>
        {numericCell(row.original.rush_max)}
        <span className={row.original.rush_max_td ? 'visible' : 'invisible'}>T</span>
      </>
    );
  },
  align: 'right',
  Header: 'Lng',
  headerAlign: 'right',
  id: 'lng',
  sortBy: ['rush_max', 'rush_max_td'],
  width: colWidth,
}, {
  accessor: 'rush_1st',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: '1st',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'rush_1st_pct',
  Cell: (item) => (numericCell(item.value, 1)),
  align: 'right',
  Header: '1st%',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'rush_20_yds',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: '20+',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'rush_40_yds',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: '40+',
  headerAlign: 'right',
  width: colWidth,
}, {
  accessor: 'fumbles_total',
  Cell: (item) => (numericCell(item.value)),
  align: 'right',
  Header: 'FUM',
  headerAlign: 'right',
  width: colWidth,
}];

export default rushingStatsColumns;
