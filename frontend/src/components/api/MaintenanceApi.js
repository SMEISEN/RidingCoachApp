/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetMaintenance = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.get(ApiPath, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQueryMaintenance = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance/query';
  axios.post(ApiPath, query, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostMaintenance = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.post(ApiPath, payload, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetMaintenanceItem = (mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.get(ApiPath, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutMaintenanceItem = (payload, mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.put(ApiPath, payload, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteMaintenanceItem = (mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.delete(ApiPath, { timeout: 15000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
