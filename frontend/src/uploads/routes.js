const API_BASE_PATH = "/api/uploads";

const UPLOAD = {
  MINIO_URL: "/api/minio/put",
  UPLOAD: `${API_BASE_PATH}/import_data`,
  LIST: `${API_BASE_PATH}/datasets_list`, // backend route for retrieving list of datasets (eg ldv_rebates)
  DOWNLOAD_SPREADSHEET: `${API_BASE_PATH}/download_dataset`,
  FILE_REQUIREMENTS: `${API_BASE_PATH}/file_requirements?dataset=:dataset`
};

export default UPLOAD;
