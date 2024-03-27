import React, { useCallback, useRef, useState } from 'react';
import { withRouter } from 'react-router-dom';

import { getFilters, getOrderBy } from '../app/utilities/reactTable';
import IcbcDataTable from './components/IcbcDataTable';
import ROUTES from './routes';
import useAxios from '../app/utilities/useAxios';

const IcbcDataContainer = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pageCount, setPageCount] = useState(-1);
  const [totalRowsCount, setTotalRowsCount] = useState(0);
  const fetchIdRef = useRef(0);
  const axios = useAxios()

  const onFetchData = useCallback((state) => {
    setLoading(true);

    fetchIdRef.current += 1;
    const fetchId = fetchIdRef.current;

    const filters = getFilters(state);

    const params = {
      ...filters,
      ordering: getOrderBy(state),
      page: state.pageIndex + 1,
      page_size: state.pageSize,
    };

    if (fetchId === fetchIdRef.current) {
      axios.get(ROUTES.LIST, { params }).then((response) => {
        const { count, results } = response.data;

        setData(results);
        setPageCount(Math.ceil(count / state.pageSize));
        setTotalRowsCount(count);
        setLoading(false);
      });
    }
  }, []);

  return (
    <div className="row">
      <div className="col-12">
        <IcbcDataTable
          data={data}
          loading={loading}
          pageCount={pageCount}
          onFetchData={onFetchData}
          totalRowsCount={totalRowsCount}
        />
      </div>
    </div>
  );
};

export default withRouter(IcbcDataContainer);
