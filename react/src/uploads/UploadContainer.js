import { withRouter } from 'react-router-dom';
import axios from 'axios';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import React, { useState, useEffect } from 'react';
import ROUTES_UPLOAD from './routes';
import UploadPage from './components/UploadPage';
import AlertDialog from '../app/components/AlertDialog';

const UploadContainer = () => {
  const [uploadFiles, setUploadFiles] = useState([]); // array of objects for files to be uploaded
  const [datasetList, setDatasetList] = useState([{}]); // holds the array of names of datasets
  const [loading, setLoading] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(''); // string identifying which dataset is being uploaded
  const [replaceData, setReplaceData] = useState('false'); // if true, we will replace all
  const [alertContent, setAlertContent] = useState();
  const [alert, setAlert] = useState(false);
  const [alertSeverity, setAlertSeverity] = useState('');
  // existing data with what is being uploaded
  const [open, setOpen] = useState(false);
  const dialogue = 'Selecting replace will delete all previously uploaded records for this dataset';
  const leftButtonText = 'Cancel';
  const rightButtonText = 'Replace existing data';
  const handleRadioChange = (event) => {
    const choice = event.target.value;
    if (choice === 'true') {
      setOpen(true);
    }
    setReplaceData(choice);
  };

  const refreshList = () => {
    setLoading(true);
    axios.get(ROUTES_UPLOAD.LIST).then((response) => {
      setDatasetList(response.data);
      setLoading(false);
    });
  };

  const showError = (error) => {
    const { response: errorResponse } = error;
    setAlertContent(errorResponse.data);
    setAlertSeverity('error');
    setAlert(true);
  };

  const doUpload = () => uploadFiles.forEach((file) => {
    axios.get(ROUTES_UPLOAD.MINIO_URL).then((response) => {
      const { url: uploadUrl, minio_object_name: filename } = response.data;
      axios.put(uploadUrl, file, {
        headers: {
          Authorization: null,
        },
      }).then(() => {
        let replace = false;
        if (replaceData === true) {
          replace = true;
        }
        axios.post(ROUTES_UPLOAD.UPLOAD, {
          filename,
          datasetSelected,
          replace,
        }).then((postResponse) => {
          setAlertContent(`Data has been successfully uploaded. ${postResponse.data}`);
          setAlertSeverity('success');
          setAlert(true);
        }).catch((error) => {
          showError(error);
        });
      }).finally(() => {
        setUploadFiles([]);
      });
    }).catch((error) => {
      const { response: errorResponse } = error;
      showError(error);
    });
  });
  const downloadSpreadsheet = () => {
    axios.get(ROUTES_UPLOAD.DOWNLOAD_SPREADSHEET, {
      params: {
        datasetSelected: datasetSelected
      },
      responseType: 'blob'
    }).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');

      link.href = url;
      link.setAttribute('download', `${datasetSelected}.xlsx`);
      document.body.appendChild(link);
      link.click();

      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    }).catch((error) => {
      showError(error);
    });
  };

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
        {alert && alertContent && alertSeverity
        && <Alert severity={alertSeverity}>{alertContent}</Alert>}
        {open && (
        <AlertDialog
          open={open}
          setOpen={setOpen}
          dialogue={dialogue}
          rightButtonText={rightButtonText}
          leftButtonText={leftButtonText}
          setReplaceData={setReplaceData}
          title="Replace existing data?"
        />
        )}
        <UploadPage
          uploadFiles={uploadFiles}
          datasetList={datasetList}
          doUpload={doUpload}
          setDatasetSelected={setDatasetSelected}
          datasetSelected={datasetSelected}
          setUploadFiles={setUploadFiles}
          setReplaceData={setReplaceData}
          replaceData={replaceData}
          handleRadioChange={handleRadioChange}
          downloadSpreadsheet={downloadSpreadsheet}
        />
      </div>
    </div>
  );
};
export default withRouter(UploadContainer);
