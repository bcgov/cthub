import PropTypes from 'prop-types';
import React from 'react';

import ReactTable from '../../app/components/ReactTable';

const IcbcDataTable = (props) => {
  const columns = [{
    accessor: 'icbc_vehicle.model_year',
    align: 'center',
    filterBy: 'icbc_vehicle__model_year__name',
    Header: 'Year',
    id: 'year',
    sortBy: 'icbc_vehicle__model_year__name',
    width: 50,
  }, {
    accessor: 'icbc_vehicle.make',
    filterBy: 'icbc_vehicle__make',
    Header: 'Make',
    headerAlign: 'left',
    id: 'make',
    sortBy: 'icbc_vehicle__make',
    width: 100,
  }, {
    accessor: 'icbc_vehicle.model_name',
    filterBy: 'icbc_vehicle__model_name',
    Header: 'Model',
    headerAlign: 'left',
    id: 'Model',
    sortBy: 'icbc_vehicle__model_name',
    width: 100,
  }, {
    accessor: 'vin',
    Header: 'VIN',
    headerAlign: 'left',
    id: 'vin',
  }];

  const {
    data, loading, onFetchData, pageCount, totalRowsCount,
  } = props;

  return (
    <ReactTable
      columns={columns}
      data={data}
      defaultSortBy={[{ id: 'vin', desc: false }]}
      loading={loading}
      onFetchData={onFetchData}
      pageCount={pageCount}
      totalRowsCount={totalRowsCount}
    />
  );
};

IcbcDataTable.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  loading: PropTypes.bool.isRequired,
  onFetchData: PropTypes.func.isRequired,
  pageCount: PropTypes.number.isRequired,
  totalRowsCount: PropTypes.number.isRequired,
};

export default IcbcDataTable;
