import axios from 'axios'
import settings from '../settings';
import useKeycloak from './useKeycloak'

const useAxios = (useDefault = false, opts = {}) => {
  if (useDefault) {
    return axios.create(opts)
  }
  const keycloak = useKeycloak()
  const instance = axios.create({
    baseURL: settings.API_BASE,
    ...opts,
  })
  instance.interceptors.request.use(async (config) => {
    if (keycloak.authenticated) {
      try {
        await keycloak.updateToken(30)
        config.headers = { 
          'Authorization': `Bearer ${keycloak.token}`,
        }
      } catch(error) {
        // do something here?
      }
    }
    return config
  })
  return instance
}

export default useAxios