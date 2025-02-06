import React, { useState, useEffect } from "react";
import useAxios from "../../app/utilities/useAxios";
import ROUTES_UPLOAD from "../routes";

const FileRequirements = ({ datasetSelected }) => {
  const axios = useAxios();
  const [requirements, setRequirements] = useState([]);

  useEffect(() => {
    if (datasetSelected) {
      axios
        .get(
          ROUTES_UPLOAD.FILE_REQUIREMENTS.replace(":dataset", datasetSelected),
        )
        .then((response) => {
          const list = [];
          for (const [key, value] of Object.entries(response.data)) {
            list.push(<li key={key}>{value}</li>);
          }
          setRequirements(list);
        })
        .catch((error) => {
          //do something here?
        });
    }
  }, [datasetSelected]);

  if (requirements.length > 0) {
    return (
      <div id="file-requirements">
        <h3>File Requirements</h3>
        <div>
          Ensure your file meets the following conditions before uploading:
        </div>
        <ul>{requirements}</ul>
      </div>
    );
  }
  return null;
};

export default FileRequirements;
