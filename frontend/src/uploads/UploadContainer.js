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
  const [totalIssueCount, setTotalIssueCount] = useState({});
  const [groupedCriticalErrors, setGroupedCriticalErrors] = useState({});
  const [groupedErrors, setGroupedErrors] = useState({});
  const [groupedWarnings, setGroupedWarnings] = useState({});
  const [alertDialogText, setAlertDialogText] = useState({
    title: "",
    content: "",
    confirmText: "",
    confirmAction: () => {},
    cancelAction: () => {},
    cancelText: "cancel",
  });
  const [failedFiles, setFailedFiles] = useState([]);
  const [fileAdjusted, setFileAdjusted] = useState(false);
  const [cleanDatasetKey, setCleanDatasetKey] = useState("")

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
          currentUserResp.data.userPermissions &&
          currentUserResp.data.userPermissions.admin === true
        ) {
          setAdminUser(true);
          setCurrentUser(currentUserResp.data.idir);
        }
      });
    });
  };

  const groupAndCountRows = (issueArray) => {
    const groupedCriticalErrors = {};
    const groupedErrors = {};
    const groupedWarnings = {};
    const totalIssueCount = {
      criticalErrors: 0,
      errors: 0,
      warnings: 0,
    };

    issueArray.forEach((issue) => {
      Object.keys(issue).forEach((column) => {
        const errorDetails = issue[column];

        Object.keys(errorDetails).forEach((errorType) => {
          const severity = errorDetails[errorType].Severity;
          const expectedType = errorDetails[errorType]["expectedType"];
          const groups = errorDetails[errorType].Groups || [];

          if (severity === "Critical") {
            const rows = errorDetails[errorType].Rows;
            const rowCount = rows.length;
            totalIssueCount.criticalErrors += rowCount;
            setFailedFiles([...failedFiles, uploadFiles]);
            setUploadFiles([]);
            if (!groupedCriticalErrors[column]) {
              groupedCriticalErrors[column] = {};
            }
            if (!groupedCriticalErrors[column][errorType]) {
              groupedCriticalErrors[column][errorType] = {
                ExpectedType: expectedType,
                Rows: rows,
              };
            } else {
              groupedCriticalErrors[column][errorType].Rows.push(...rows);
            }
          } else if (severity === "Error") {
            const rows = errorDetails[errorType].Rows || null;
            const rowCount = rows.length || groups.length;
            totalIssueCount.errors += rowCount;

            if (!groupedErrors[column]) {
              groupedErrors[column] = {};
            }
            if (!groupedErrors[column][errorType]) {
              groupedErrors[column][errorType] = {
                ExpectedType: expectedType,
                Rows: [...rows],
              };
            } else {
              groupedErrors[column][errorType].Rows.push(...rows);
            }
          } else if (severity === "Warning") {
            let warningRowCount = 0;

            if (!groupedWarnings[column]) {
              groupedWarnings[column] = {};
            }
            if (!groupedWarnings[column][errorType]) {
              groupedWarnings[column][errorType] = {
                ExpectedType: expectedType,
                Groups: [],
              };
            }

            groups.forEach((group) => {
              groupedWarnings[column][errorType].Groups.push(group);
              warningRowCount += group.Rows.length;
            });

            totalIssueCount.warnings += warningRowCount;
          }
        });
      });
    });

    return {
      groupedCriticalErrors,
      groupedErrors,
      groupedWarnings,
      totalIssueCount,
    };
  };
  const clearErrors = () => {
    setGroupedCriticalErrors({});
    setGroupedErrors({});
    setGroupedWarnings({});
    setTotalIssueCount({});
  };

  const showError = (error) => {
    const { response: errorResponse } = error;
    setAlertContent("There was an issue uploading the file.");
    if (errorResponse && errorResponse.data && errorResponse.data.message) {
      setAlertContent(
        `${errorResponse.data.message}\n${errorResponse.data.errors ? "Errors: " + errorResponse.data.errors.join("\n") : ""}`,
      );
    } else if (
      errorResponse &&
      errorResponse.data &&
      errorResponse.status === 403
    ) {
      setAlertContent(
        "There was an error. Please refresh page and ensure you are logged in.",
      );
    }
    setAlertSeverity("error");
    setAlert(true);
  };

  const doUpload = (checkForWarnings) => {
    setLoading(true);

    const uploadPromises = uploadFiles.map((file) => {
      let filepath = file.path;
      return axios.get(ROUTES_UPLOAD.MINIO_URL).then((response) => {
        const { url: uploadUrl, minioObjectName: filename } = response.data;
        return axiosDefault.put(uploadUrl, file).then(() => {
          return axios.post(ROUTES_UPLOAD.UPLOAD, {
            filename,
            datasetSelected,
            replaceData,
            filepath,
            checkForWarnings,
          });
        });
      });
    });

    Promise.all(uploadPromises)
      .then((responses) => {
        const errorCheck = responses.some((response) => !response.data.success);
        setAlertSeverity(errorCheck ? "error" : "success");
        const message = responses
          .map(
            (response) =>
              `${response.data.message}${response.data.errors ? "\nErrors: " + response.data.errors.join("\n") : ""}`,
          )
          .join("\n");
        
        if(!errorCheck && responses.some((response) => !response.data.warning)){
          setAlert(true);
          setAlertContent(message);
        }

        const fileAdjustedResponse = responses.some((response) => response.data.fileAdjusted);
        setFileAdjusted(fileAdjustedResponse);

        const cleanDatasetKeyResponse = responses.find(
          (response) => response.data.cleanedDatasetKey
        )?.data.cleanedDatasetKey;
        
        setCleanDatasetKey(cleanDatasetKeyResponse || "")

        const warnings = {};
        responses.forEach((response, index) => {
          const responseWarnings = response.data.errorsAndWarnings;
          if (responseWarnings) {
            warnings[uploadFiles[index].name] = responseWarnings;
          }
        });

        if (Object.keys(warnings).length > 0 && checkForWarnings) {
          const {
            groupedCriticalErrors,
            groupedErrors,
            groupedWarnings,
            totalIssueCount,
          } = groupAndCountRows(Object.values(warnings));

          setGroupedCriticalErrors(groupedCriticalErrors);
          setGroupedErrors(groupedErrors);
          setGroupedWarnings(groupedWarnings);
          setTotalIssueCount(totalIssueCount);
          setAlertDialogText({
            title:
              totalIssueCount.criticalErrors > 0
                ? "File upload failed"
                : "Your file has been processed and contains the following errors and warnings!",
            content: (
              <>
                {totalIssueCount.criticalErrors >= 1 && (
                  <div>
                    {groupedCriticalErrors &&
                      groupedCriticalErrors.Spreadsheet &&
                      groupedCriticalErrors.Spreadsheet[
                        "Missing Worksheet"
                      ] && (
                        <div>
                          File Upload Failed - The sheet name doesn't match the
                          required “
                          {
                            groupedCriticalErrors.Spreadsheet[
                              "Missing Worksheet"
                            ].Rows[0]
                          }
                          ”.
                          <br />
                        </div>
                      )}
                    {groupedCriticalErrors &&
                      groupedCriticalErrors.Headers &&
                      groupedCriticalErrors.Headers["Missing Headers"] && (
                        <div>
                          The file is missing one or more required columns.
                        </div>
                      )}
                  </div>
                )}
                {totalIssueCount.errors >= 1 && (
                  <div>
                    <span className="error">
                      {totalIssueCount.errors} Errors
                    </span>
                    - Must fix before uploading
                  </div>
                )}
                {totalIssueCount.warnings >= 1 && (
                  <div>
                    <span className="warning">
                      {totalIssueCount.warnings} Warnings
                    </span>
                    - Can upload without fixing
                  </div>
                )}
              </>
            ),
            cancelAction: () => {
              setOpenDialog(false);
              clearErrors();
              setUploadFiles([]);
            },
            confirmText: "View Details",
            confirmAction: () => setOpenDialog(false),
          });
          setOpenDialog(true);
        }
      })
      .catch((error) => {
        showError(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

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
        content:
          "Selecting replace will delete all previously uploaded records for this dataset",
        confirmText: "Replace existing data",
        confirmAction: handleReplaceDataConfirm,
        cancelAction: handleReplaceDataCancel,
      });
    } else {
      setReplaceData(false);
    }
  };

  const handleConfirmDataInsert = () => {
    setGroupedWarnings({});
    setGroupedErrors({});
    setTotalIssueCount({});
    setOpenDialog(false);
    setAlert(false);
    setAlertContent("");
    doUpload(false); // Upload with the checkForWarnings flag set to false!
    setUploadFiles([]);
  };

  const handleReplaceDataConfirm = () => {
    setReplaceData(true);
    setOpenDialog(false);
  };

  const handleReplaceDataCancel = () => {
    setOpenDialog(false);
  };

  useEffect(() => {
    refreshList();
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
            title={alertDialogText.title}
            dialogue={alertDialogText.content} // Corrected prop name
            cancelText={alertDialogText.cancelText}
            handleCancel={alertDialogText.cancelAction}
            confirmText={alertDialogText.confirmText}
            handleConfirm={alertDialogText.confirmAction}
          />
          <Stack direction="column" spacing={2}>
            {(totalIssueCount.criticalErrors ||
              totalIssueCount.errors > 0 ||
              totalIssueCount.warnings > 0) && (
              <Paper variant="outlined" square elevation={0} sx={{ mb: 2 }}>
                <UploadIssues
                  confirmUpload={handleConfirmDataInsert}
                  groupedCriticalErrors={groupedCriticalErrors}
                  groupedErrors={groupedErrors}
                  groupedWarnings={groupedWarnings}
                  totalIssueCount={totalIssueCount}
                  clearErrors={clearErrors}
                  setUploadFiles={setUploadFiles}
                />
              </Paper>
            )}
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
                totalIssueCount={totalIssueCount}
                clearErrors={clearErrors}
                failedFiles={failedFiles}
                fileAdjusted={fileAdjusted}
                cleanDatasetKey={cleanDatasetKey}
              />
            </Paper>
            {adminUser && (
              <Paper square variant="outlined" sx={{ mt: 2 }}>
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
