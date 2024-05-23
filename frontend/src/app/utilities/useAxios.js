import axios from "axios";
import useKeycloak from "./useKeycloak";
import { API_BASE } from "../../config";
import { useHistory } from "react-router-dom";

const useAxios = (useDefault = false, opts = {}) => {
  const history = useHistory();
  const keycloak = useKeycloak();
  if (useDefault) {
    return axios.create(opts);
  }
  const instance = axios.create({
    baseURL: API_BASE,
    ...opts,
  });
  instance.interceptors.request.use(async (config) => {
    if (keycloak.authenticated) {
      try {
        await keycloak.updateToken(30);
        config.headers = {
          Authorization: `Bearer ${keycloak.token}`,
        };
      } catch (error) {
        keycloak.logout();
        history.push("/upload");
      }
    }
    return config;
  });
  return instance;
};

export default useAxios;
