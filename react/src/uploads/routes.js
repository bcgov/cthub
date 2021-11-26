const API_BASE_PATH = '/uploads';

const UPLOAD = {
  MINIO_URL: '/api/minio/put',
  UPLOAD: `${API_BASE_PATH}/upload`, // backend route for uploading data
  LIST: `${API_BASE_PATH}/datasetList/`, // backend route for retrieving list of datasets (eg ldv_rebates)
};

export default UPLOAD;
