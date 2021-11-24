import { withRouter } from 'react-router-dom';
import axios from 'axios';
import React, { useState, useCallback } from 'react';
import ROUTES from './routes';
import UploadPage from './components/UploadPage';

const UploadContainer = () => {
  const [data, setData] = useState([]);
  const [uploadFiles, setUploadFiles] = useState([]);
  const [datasetList, setDatasetLists] = useState(['LDV rebates']);
  const [loading, setLoading] = useState(false);
  const onFetchData = useCallback((state) => {
    setLoading(true);
    // axios.get(ROUTES.LIST).then((response) => {
    // eventually we will retrieve list of input options
    // });
  }, []);
  const doUpload = () => uploadFiles.forEach((file) => {
    console.log(uploadFiles)
    // axios.get(ROUTES_UPLOADS.MINIO_URL).then((response) => {
    //   const { url: uploadUrl, minioObjectName: filename } = response.data;
    //   axios.put(uploadUrl, file, {
    //     headers: {
    //       Authorization: null,
    //     },
    //   }).catch((error) => {
    //     console.error(error);
    //     const { response: errorResponse } = error;
    //     console.log(errorResponse.data);
    //   }).finally(() => {
    //     setUploadFiles([]);
    //   });
    // }).catch((error) => {
    //   console.error(error);
    // });
  });

  return (
    <div className="row">
      <div className="col-12 mr-2">
        <UploadPage
          uploadFiles={uploadFiles}
          data={data}
          datasetList={datasetList}
          doUpload={doUpload}
        />
      </div>
    </div>
  );
};
export default withRouter(UploadContainer);
