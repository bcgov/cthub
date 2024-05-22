import { withRouter } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Paper, Alert, Stack } from "@mui/material";
import ROUTES_UPLOAD from "./routes";
import ROUTES_USERS from "../users/routes";
import UploadPage from "./components/UploadPage";
import AlertDialog from "../app/components/AlertDialog";
import UsersContainer from "../users/UsersContainer";
import Loading from "../app/components/Loading";
import useAxios from "../app/utilities/useAxios";

const UploadContainer = () => {
  const [uploadFiles, setUploadFiles] = useState([]); // array of objects for files to be uploaded
  const [datasetList, setDatasetList] = useState([{}]); // holds the array of names of datasets
  const [loading, setLoading] = useState(false);
  const [refresh, setRefresh] = useState(false); // Used for page refresh instead of loading progress
  const [datasetSelected, setDatasetSelected] = useState(""); // string identifying which dataset is being uploaded
  const [replaceData, setReplaceData] = useState(false); // if true, we will replace all
  const [alertContent, setAlertContent] = useState();
  const [alert, setAlert] = useState(false);
  const [currentUser, setCurrentUser] = useState("");
  const [alertSeverity, setAlertSeverity] = useState("");
  const [openDialog, setOpenDialog] = useState(false);
  const [adminUser, setAdminUser] = useState(false);
  const axios = useAxios();
  const axiosDefault = useAxios(true);

  const refreshList = () => {
    setRefresh(true);
    axios.get(ROUTES_UPLOAD.LIST).then((response) => {
      setDatasetList(response.data);
      setRefresh(false);
      axios.get(ROUTES_USERS.CURRENT).then((currentUserResp) => {
        if (
          currentUserResp.data &&
          currentUserResp.data.user_permissions &&
          currentUserResp.data.user_permissions.admin === true
        ) {
          setAdminUser(true);
          setCurrentUser(currentUserResp.data.idir);
        }
      });
    });
  };

  const showError = (error) => {
    const { response: errorResponse } = error;
    setAlertContent("There was an issue uploading the file.")
    if (errorResponse && errorResponse.data && errorResponse.data.message) {
      setAlertContent(
        `${errorResponse.data.message}\n${errorResponse.data.errors ? "Errors: " + errorResponse.data.errors.join("\n") : ""}`,
      )
    } else if (errorResponse && errorResponse.data && errorResponse.status === 403) {
      setAlertContent("There was an error. Please refresh page and ensure you are logged in.")
    }
    setAlertSeverity("error");
    setAlert(true);
  };

  const doUpload = () =>
    uploadFiles.forEach((file) => {
      let filepath = file.path;
      setLoading(true);
      const uploadPromises = uploadFiles.map((file) => {
        return axios.get(ROUTES_UPLOAD.MINIO_URL).then((response) => {
          const { url: uploadUrl, minio_object_name: filename } = response.data;
          return axiosDefault.put(uploadUrl, file).then(() => {
            let replace = false;
            if (replaceData === true) {
              replace = true;
            }
            return axios.post(ROUTES_UPLOAD.UPLOAD, {
              filename,
              datasetSelected,
              replace,
              filepath,
            });
          });
        });
      });

      Promise.all(uploadPromises)
        .then((responses) => {
          const errorCheck = responses.some(
            (response) => response.data.success,
          );

          setAlertSeverity(errorCheck ? "success" : "error");

          const message = responses
            .map(
              (response) =>
                `${response.data.message}${response.data.errors ? "\nErrors: " + response.data.errors.join("\n") : ""}`,
            )
            .join("\n");

          setAlertContent(message);
          setAlert(true);
          setUploadFiles([]);
        })
        .catch((error) => {
          showError(error);
        })
        .finally(() => {
          setLoading(false);
        });
    });

  const downloadSpreadsheet = () => {
    axios
      .get(ROUTES_UPLOAD.DOWNLOAD_SPREADSHEET, {
        params: {
          datasetSelected,
        },
        responseType: "blob",
      })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");

        link.href = url;
        link.setAttribute("download", `${datasetSelected}.xlsx`);
        document.body.appendChild(link);
        link.click();

        link.parentNode.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        showError(error);
      });
  };

  const handleRadioChange = (event) => {
    const choice = event.target.value;
    if (choice === "replace") {
      setOpenDialog(true);
    } else {
      setReplaceData(false);
    }
  };

  const handleReplaceDataConfirm = () => {
    setReplaceData(true);
    setOpenDialog(false);
  };

  const handleReplaceDataCancel = () => {
    setOpenDialog(false);
  };

  useEffect(() => {
    refreshList(true);
  }, []);

  if (refresh) {
    return <Loading />;
  }

  const alertElement =
    alert && alertContent && alertSeverity ? (
      <Alert severity={alertSeverity}>
        {alertContent.split("\n").map((line, index) => (
          <React.Fragment key={index}>
            {line}
            <br />
          </React.Fragment>
        ))}
      </Alert>
    ) : null;

  return (
    <div className="row">
      <div className="col-12 mr-2">
        <>
          <AlertDialog
            open={openDialog}
            title={"Replace existing data?"}
            dialogue={
              "Selecting replace will delete all previously uploaded records for this dataset"
            }
            cancelText={"Cancel"}
            handleCancel={handleReplaceDataCancel}
            confirmText={"Replace existing data"}
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
                loading={loading}
              />
            </Paper>
            {adminUser && (
              <Paper square variant="outlined">
                <UsersContainer currentUser={currentUser} />
              </Paper>
            )}
          </Stack>
        </>
      </div>
    </div>
  );
};
export default withRouter(UploadContainer);
