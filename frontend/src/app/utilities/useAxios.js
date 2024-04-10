import axios from "axios";
import useKeycloak from "./useKeycloak";
import { API_BASE } from "../../config";

const useAxios = (useDefault = false, opts = {}) => {
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
        // do something here?
      }
    }
    return config;
  });
  return instance;
};

export default useAxios;
