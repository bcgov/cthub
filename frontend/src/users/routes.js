const API_BASE_PATH = "/api/users";

const USERS = {
  LIST: API_BASE_PATH,
  CURRENT: `${API_BASE_PATH}/current`,
  CREATE: API_BASE_PATH,
  UPDATE: `${API_BASE_PATH}/update_permissions`,
  DETAILS: `${API_BASE_PATH}/:id`,
};

export default USERS;
