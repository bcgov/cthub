import { withRouter } from 'react-router-dom';
import axios from 'axios';
import CircularProgress from '@material-ui/core/CircularProgress';
import React, { useState, useEffect } from 'react';
import ROUTES_UPLOAD from './routes'
import UploadPage from './components/UploadPage';

const UploadContainer = () => {
  const [uploadFiles, setUploadFiles] = useState([]); // array of objects for files to be uploaded
  const [datasetList, setDatasetList] = useState(['LDV rebates']); //holds the array of names of datasets
  const [loading, setLoading] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(''); //string identifying which dataset is being uploaded
  const refreshList = () => {
    // setLoading(true);
    // axios.get(ROUTES.LIST).then((response) => {
    //   setDatasetList(response.data);
    //   setLoading(false);
    // });
  };
  const doUpload = () => uploadFiles.forEach((file) => {
    axios.get(ROUTES_UPLOAD.MINIO_URL).then((response) => {
      const { url: uploadUrl, minio_object_name: filename } = response.data;
      axios.put(uploadUrl, file, {
        headers: {
          Authorization: null,
        },
      }).then(() => {
        axios.post(ROUTES_UPLOAD.UPLOAD, {
          filename,
        });
      }).catch((error) => {
        console.error(error);
        const { response: errorResponse } = error;
        console.log(errorResponse.data);
      }).finally(() => {
        setUploadFiles([]);
      });
    }).catch((error) => {
      console.error(error);
    });
  });
  useEffect(() => {
    refreshList(true);
  }, []);
  if (loading) {
    return (
      <div>
        <CircularProgress color="inherit" />
      </div>
    );
  }
  return (
    <div className="row">
      <div className="col-12 mr-2">
        <UploadPage
          uploadFiles={uploadFiles}
          datasetList={datasetList}
          doUpload={doUpload}
          setDatasetSelected={setDatasetSelected}
          datasetSelected={datasetSelected}
          setUploadFiles={setUploadFiles}
        />
      </div>
    </div>
  );
};
export default withRouter(UploadContainer);
