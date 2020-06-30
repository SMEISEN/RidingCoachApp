/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetMaintenance = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiQueryMaintenance = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance/query';
  axios.post(ApiPath, query)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
