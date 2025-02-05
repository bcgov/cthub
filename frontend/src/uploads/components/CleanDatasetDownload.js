import React from "react";
import useAxios from "../../app/utilities/useAxios";
import ROUTES_UPLOAD from "../routes";
import { Button, Box } from "@mui/material";

const CleanDatasetDownload = ({ cleanDatasetKey }) => {
  const axios = useAxios();
  const axiosDefault = useAxios(true);

  const handleDownload = () => {
    axios
      .get(ROUTES_UPLOAD.DOWNLOAD_CLEAN_DATA, {
        params: { key: cleanDatasetKey },
      })
      .then((response) => {
        const { presigned_url } = response.data;

        axiosDefault
          .get(presigned_url, { responseType: "blob" })
          .then((fileResponse) => {
            const url = window.URL.createObjectURL(new Blob([fileResponse.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "clean_dataset.xlsx");
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
          })
          .catch((error) => {
            alert("Failed to download the file. Please try again.");
          });
      })
      .catch((error) => {
        alert("Failed to generate the download link. Please try again.");
      });
  };

  return (
    <Box id="clean-dataset-download" sx={{ margin: "20px 0" }}>
      <Box sx={{ marginBottom: "20px" }}>
        <h3>Clean Dataset Download</h3>
      </Box>
      <Box sx={{ marginBottom: "20px" }}>
        <p>
          Your file has been adjusted to improve consistency (e.g., formatting changes such as capitalizing column headers).{" "}
          <b>No content was added or removed from the dataset.</b>
        </p>
        <p>You can download the updated version below to review:</p>
      </Box>
      <Button
        className="button-dark-blue button-lowercase"
        type="button"
        variant="contained"
        onClick={handleDownload}
        sx={{ marginBottom: "20px" }}
      >
        Download
      </Button>
    </Box>
  );
};

export default CleanDatasetDownload;