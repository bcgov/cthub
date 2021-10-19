import PropTypes from 'prop-types';
import React from 'react';
// import ReactTable from 'react-table';

import ReactTable from '../../app/components/ReactTable';
import playerColumns from './RushingStatsTable/playerColumns';
import rushingStatsColumns from './RushingStatsTable/rushingStatsColumns';
import teamColumns from './RushingStatsTable/teamColumns';

const RushingStatsTable = (props) => {
  const columns = [{
    columns: playerColumns,
    filterable: false,
    Header: 'Player',
    sortable: false,
  }, {
    columns: teamColumns,
    filterable: false,
    Header: 'Team',
    sortable: false,
  }, {
    columns: rushingStatsColumns,
    filterable: false,
    Header: 'Rushing Stats',
    sortable: false,
  }];

  const {
    data, loading, onFetchData, pageCount, totalRowsCount,
  } = props;

  return (
    <ReactTable
      columns={columns}
      data={data}
      defaultSortBy={[{ id: 'player-name', desc: false }]}
      loading={loading}
      onFetchData={onFetchData}
      pageCount={pageCount}
      totalRowsCount={totalRowsCount}
    />
  );
};

RushingStatsTable.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  loading: PropTypes.bool.isRequired,
  onFetchData: PropTypes.func.isRequired,
  pageCount: PropTypes.number.isRequired,
  totalRowsCount: PropTypes.number.isRequired,
};

export default RushingStatsTable;
