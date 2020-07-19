/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetSetups = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostSetup = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.post(ApiPath, payload, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutSetupItem = (payload, setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.put(ApiPath, payload, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.delete(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
