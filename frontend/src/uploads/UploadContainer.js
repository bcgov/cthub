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
import WarningsList from "./components/WarningsList";
import UploadIssues from "./components/UploadIssues";

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
  const [uploadIssueArray, setUploadIssueArray] = useState(
    [{"Column": "Date",
    "Error Type": "The date must be in the proper format",
    "Expected Format": "YYYY-MM-DD", 
    "Severity": "Error",
    "Rows": [1,2,3],
   },
{   "Column": "Applicant Name",
    "Error Type": "contains null values ",
    "Expected Format": "Smith, John", 
    "Severity": "Error",
    "Rows": [4,6]
  },
{    "Column": "Phone",
    "Error Type": "phone number not formatted correctly ",
    "Expected Format": "213-1234-1231",
    "Severity": "Warning",
    "Rows": [7,8,9]
   },
{    "Column": "Company Name",
    "Error Type": "contains null values ",
    "Expected Format": "Smith, John",  
    "Severity": "Warning",
    "Rows": [9, 12,13, 14,15,16,17,28,27,43,23,2323,23,23,65,342,23,7,56,53,56,67,78,89,45,3,2,1, 54, 56, 76,78,79,90,34,23,22,21,255,26,27,27,28]
   }
  ]);
  const [alertDialogText, setAlertDialogText] = useState({
    title: "",
    content: "",
    confirmText: "",
    confirmAction: ()=>{},
    cancelAction: ()=>{},
    cancelText: "cancel"
  })
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

  const doUpload = (checkForWarnings) =>
    uploadFiles.forEach((file) => {
      let filepath = file.path;
      setLoading(true);   
      if (datasetSelected !== 'Go Electric Rebates Program'){
        checkForWarnings = false
      }
      const uploadPromises = uploadFiles.map((file) => {
        return axios.get(ROUTES_UPLOAD.MINIO_URL).then((response) => {
          const { url: uploadUrl, minio_object_name: filename } = response.data;
          return axiosDefault.put(uploadUrl, file).then(() => {
            return axios.post(ROUTES_UPLOAD.UPLOAD, {
              filename,
              datasetSelected,
              replaceData,
              filepath,
              checkForWarnings
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
          setAlert(true);
          setAlertContent(message);
          const warnings = {}
          for (const [index, response] of responses.entries()) {
            const filename = uploadFiles[index].name
            const responseWarnings = response.data.warnings
            if (responseWarnings) {
              warnings[filename] = responseWarnings
            }
          }
          setAlertContent(message);

          if (Object.keys(warnings).length > 0 && checkForWarnings == true) { // ie it is the first attempt to upload (when upload is called from the dialog its set to false)
            
            //popup for showing issues
            setAlertDialogText({
              title: "Your file has been processed and contains the following errors and warnings!",
              content:(
                <>
                <div>
                  {/* {*errors* &&  */}
                    <p>
                      <span className="error">48 Errors </span>- Must fix before uploading
                    </p>
                  {/* } */}
                  {/* {*warnings* &&  */}
                    <p>
                      <span className="warning">14 Warnings </span>- Can upload without fixing
                    </p>
                  {/* } */}
                </div>
                </>
            ),
              cancelText: "View Details", 
              cancelAction: ()=> setOpenDialog(false),
            })
          setOpenDialog(true)
          }

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
      //popup for replacing data
      setAlertDialogText({
        title: "Replace existing data?",
        content: "Selecting replace will delete all previously uploaded records for this dataset",
        confirmText: "Replace existing data", 
        confirmAction: handleReplaceDataConfirm,
        cancelAction: handleReplaceDataCancel,
      })
    } else {
      setReplaceData(false);
    }
  };
  const handleConfirmDataInsert = () => {
    setOpenDialog(false);
    showError(false);
    setAlertContent("")
    doUpload(false); //upload with the checkForWarnings flag set to false!

  }
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
  //on page alert
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

   //on page alert
    // alert && alertContent && alertSeverity ? (
    //   <UploadIssues alertSeverity={alertSeverity} alertContent={alertContent}/>
    // ) : null;
  return (
    <div className="row">
      <div className="col-12 mr-2">
        <>
        {uploadIssueArray &&
          <UploadIssues issues={uploadIssueArray}/>
        }
          <AlertDialog
          // popup
            open={openDialog}
            title={alertDialogText.title}
            dialogue={
              alertDialogText.content
            }
            cancelText={alertDialogText.cancelText}
            handleCancel={alertDialogText.cancelAction}
            confirmText={alertDialogText.confirmText}
            handleConfirm={alertDialogText.confirmAction}
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
