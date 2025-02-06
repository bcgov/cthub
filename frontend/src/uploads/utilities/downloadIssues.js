const getSpreadsheetRows = (issues) => {
  const result = [];
  if (issues) {
    for (const [columnName, value] of Object.entries(issues)) {
      for (const [issueName, innerValue] of Object.entries(value)) {
        const expectedValue =
          innerValue.ExpectedType || innerValue.ExpectedFormat;
        const rows = innerValue.Rows;
        const groups = innerValue.Groups;
        const [isGroup, items] = rows ? [false, [rows]] : [true, groups];
        for (const item of items) {
          result.push({
            "Column Name": columnName,
            Issue: issueName,
            "Expected Value": expectedValue,
            Rows: isGroup ? concatGroup(item) : concatRow(item),
          });
        }
      }
    }
  }
  return result;
};

const concatGroup = (group) => {
  let result = "";
  if (group) {
    if (group.Rows) {
      result = group.Rows.join(", ");
      for (const groupKey of Object.keys(group)) {
        if (groupKey !== "Rows") {
          result = result + " - " + group[groupKey];
        }
      }
    }
  }
  return result;
};

const concatRow = (row) => {
  let result = "";
  if (row) {
    result = row.join(", ");
  }
  return result;
};

export default getSpreadsheetRows;
