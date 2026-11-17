import axios from "axios";
import useKeycloak from "./useKeycloak";
import { API_BASE } from "../../config";
import { useNavigate } from "react-router-dom";

const useAxios = (useDefault = false, opts = {}) => {
  const navigate = useNavigate();
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
        navigate("/upload");
      }
    }
    return config;
  });
  return instance;
};

export default useAxios;
