import { withRouter } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import {
  Paper, Alert, Stack,
} from '@mui/material';
import ROUTES_UPLOAD from './routes';
import ROUTES_USERS from '../users/routes';
import UploadPage from './components/UploadPage';
import AlertDialog from '../app/components/AlertDialog';
import UsersContainer from '../users/UsersContainer';
import Loading from '../app/components/Loading';
import useAxios from '../app/utilities/useAxios';

const UploadContainer = () => {
  const [uploadFiles, setUploadFiles] = useState([]); // array of objects for files to be uploaded
  const [datasetList, setDatasetList] = useState([{}]); // holds the array of names of datasets
  const [loading, setLoading] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(''); // string identifying which dataset is being uploaded
  const [replaceData, setReplaceData] = useState(false); // if true, we will replace all
  const [alertContent, setAlertContent] = useState();
  const [alert, setAlert] = useState(false);
  const [currentUser, setCurrentUser] = useState('');
  const [alertSeverity, setAlertSeverity] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [adminUser, setAdminUser] = useState(false);
  const axios = useAxios();
  const axiosDefault = useAxios(true);

  const refreshList = () => {
    setLoading(true);
    axios.get(ROUTES_UPLOAD.LIST).then((response) => {
      setDatasetList(response.data);
      setLoading(false);
      axios.get(ROUTES_USERS.CURRENT).then((currentUserResp) => {
        if (currentUserResp.data.user_permissions.admin === true) {
          setAdminUser(true);
          setCurrentUser(currentUserResp.data.idir);
        }
      });
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
      axiosDefault.put(uploadUrl, file).then(() => {
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
        datasetSelected,
      },
      responseType: 'blob',
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

  const handleRadioChange = (event) => {
    const choice = event.target.value;
    if (choice === 'replace') {
      setOpenDialog(true);
    } else {
      setReplaceData(false);
    }
  };

  const handleReplaceDataConfirm = () => {
    setReplaceData(true)
    setOpenDialog(false)
  }

  const handleReplaceDataCancel = () => {
    setOpenDialog(false)
  }

  useEffect(() => {
    refreshList(true);
  }, []);

  if (loading) {
    return <Loading />;
  }

  const alertElement = alert && alertContent && alertSeverity ? <Alert severity={alertSeverity}>{alertContent}</Alert> : null

  return (
    <div className="row">
      <div className="col-12 mr-2">
        <AlertDialog
          open={openDialog}
          title={'Replace existing data?'}
          dialogue={'Selecting replace will delete all previously uploaded records for this dataset'}
          cancelText={'Cancel'}
          handleCancel={handleReplaceDataCancel}
          confirmText={'Replace existing data'}
          handleConfirm={handleReplaceDataConfirm}
        />
        <Stack direction="column" spacing={2}>
          <Paper square variant="outlined">
            <UploadPage
              alertElement={alertElement}
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
              setAlert={setAlert}
            />
          </Paper>
          {adminUser
          && (
            <Paper square variant="outlined">
              <UsersContainer currentUser={currentUser} />
            </Paper>
          )}
        </Stack>
      </div>
    </div>
  );
};
export default withRouter(UploadContainer);
