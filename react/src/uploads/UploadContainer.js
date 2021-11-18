import axios from 'axios';
import React, { useState, useCallback } from 'react';
import ROUTES from './routes';

const UploadContainer = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const onFetchData = useCallback((state) => {
    setLoading(true);
    // axios.get(ROUTES.LIST).then((response) => {
    // eventually we will retrieve list of input options
    // });
  }, []);

  return (
    <div className="row">
      <div className="col-12">
        hi
      </div>
    </div>
  );
};
export default UploadContainer;
