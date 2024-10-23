import React from "react";

const WarningsList = ({ warnings = {} }) => {
  const warningElements = [];
  for (const [filename, value] of Object.entries(warnings)) {
    for (const [warningType, warning] of Object.entries(value)) {
      for (const [column, indices] of Object.entries(warning)) {
        const indicesString = indices.join(", ");
        // todo: remove inline styling once we know more about the UI
        const warningElement = (
          <div style={{ "margin-bottom": "10px" }}>
            {`The file "${filename}" contains warnings of type "${warningType}" located under column "${column}", and along row(s): `}{" "}
            <strong>{indicesString}</strong>
          </div>
        );
        warningElements.push(warningElement);
      }
    }
  }
  if (Object.keys(warningElements).length > 0) {
    return <div>{warningElements}</div>;
  }
  return null;
};

export default WarningsList;
