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

  const groupAndCountRows = (issueArray) => {
    const groupedErrors = {};
    const groupedWarnings = {};
    const totalIssueCount = {
      errors: 0,
      warnings: 0,
    };

    issueArray.forEach((issue) => {
      const column = Object.keys(issue)[0];
      const errorDetails = issue[column];

      Object.keys(errorDetails).forEach((errorType) => {
        const severity = errorDetails[errorType].Severity;
        const expectedType = errorDetails[errorType]["Expected Type"];
        const expectedFormat = errorDetails[errorType]["Expected Format"];
        const rows = errorDetails[errorType].Rows;
        const rowCount = rows.length;

        if (severity === "Error") {
          totalIssueCount.errors += rowCount;
          if (!groupedErrors[column]) {
            groupedErrors[column] = {};
          }
          if (!groupedErrors[column][errorType]) {
            groupedErrors[column][errorType] = {
              ExpectedType: expectedType,
              Rows: rows,
            };
          }
        } else if (severity === "Warning") {
          totalIssueCount.warnings += rowCount;
          if (!groupedWarnings[column]) {
            groupedWarnings[column] = {};
          }
          if (!groupedWarnings[column][errorType]) {
            groupedWarnings[column][errorType] = {
              ExpectedFormat: expectedFormat,
              Rows: rows,
            };
          }
        }
      });
    });

    return { groupedErrors, groupedWarnings, totalIssueCount };
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
    uploadFiles.forEach((file) => {
      let filepath = file.path;
      setLoading(true);
      if (datasetSelected !== "Go Electric Rebates Program") {
        checkForWarnings = false;
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
              checkForWarnings,
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
          const warnings = {};
          for (const [index, response] of responses.entries()) {
            const filename = uploadFiles[index].name;
            const responseWarnings = response.data.warnings;
            if (responseWarnings) {
              warnings[filename] = responseWarnings;
            }
          }
          setAlertContent(message);

          if (Object.keys(warnings).length > 0 && checkForWarnings === true) {
            // ie it is the first attempt to upload (when upload is called from the dialog its set to false)
            const fakeResponse = [
              {
                // 'Applicant Name': {
                //   "blank": {
                //     "Expected Type": "must not be blank",
                //     Severity: "Error",
                //     Rows: [
                //       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                //       18, 19, 20, 21, 22, 23, 24,
                //     ],
                //   },
                // },
                'Phone': {
                  "phone number not formatted correctly": {
                    "Expected Type": "213-1234-1231",
                    Severity: "Warning",
                    Rows: [
                      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                      18, 19, 20, 21, 22, 23, 24,
                    ],
                  },
                },
              },
              {
                "Company Name": {
                  "contains null values": {
                    "Expected Format": "Smith, John",
                    Severity: "Warning",
                    Rows: [
                      9, 12, 13, 14, 15, 16, 17, 28, 27, 43, 23, 2323, 24, 25,
                      65, 342, 23, 7, 56, 53, 56, 67, 78, 89, 45, 3, 2, 1, 54,
                      56, 76, 78, 79, 90, 34, 23, 22, 21, 255, 26, 27, 27, 28,
                    ],
                  },
                },
              },
            ];
            // Call groupAndCountRows to get data and pass to state
            const { groupedErrors, groupedWarnings, totalIssueCount } =
              groupAndCountRows(fakeResponse);
            setGroupedErrors(groupedErrors);
            setGroupedWarnings(groupedWarnings);
            setTotalIssueCount(totalIssueCount);
            //popup for showing issues
            setAlertDialogText({
              title:
                "Your file has been processed and contains the following errors and warnings!",
              content: (
                <>
                  {totalIssueCount.errors >= 1 && (
                    <div>
                      <span className="error">
                        {totalIssueCount.errors} Errors
                      </span>{" "}
                      - Must fix before uploading
                    </div>
                  )}
                  {totalIssueCount.warnings >= 1 && (
                    <div>
                      <span className="warning">
                        {totalIssueCount.warnings} Warnings
                      </span>{" "}
                      - Can upload without fixing
                    </div>
                  )}
                </>
              ),
              cancelAction: () => setOpenDialog(false),
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
    setGroupedWarnings({})
    setGroupedErrors({})
    setTotalIssueCount({})
    setOpenDialog(false);
    setAlert(false);
    setAlertContent("");
    doUpload(false); // Upload with the checkForWarnings flag set to false!
    setUploadFiles([])
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
            dialogue={alertDialogText.content}
            cancelText={alertDialogText.cancelText}
            handleCancel={alertDialogText.cancelAction}
            confirmText={alertDialogText.confirmText}
            handleConfirm={alertDialogText.confirmAction}
          />
          <Stack direction="column" spacing={2}>
            {(totalIssueCount.errors > 0 || totalIssueCount.warnings > 0) && (
              <Paper variant="outlined" square elevation={0} sx={{ mb: 2 }}>
                <UploadIssues
                  confirmUpload={handleConfirmDataInsert}
                  groupedErrors={groupedErrors}
                  groupedWarnings={groupedWarnings}
                  totalIssueCount={totalIssueCount}
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
