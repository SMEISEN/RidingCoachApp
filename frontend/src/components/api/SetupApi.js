/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetSetups = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPostSetup = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiGetSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPutSetupItem = (payload, setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiDeleteSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
