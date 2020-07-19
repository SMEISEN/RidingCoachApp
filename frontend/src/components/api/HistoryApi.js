/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetHistory = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQueryHistory = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history/query';
  axios.post(ApiPath, query, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostHistory = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.post(ApiPath, payload, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetHistoryItem = (histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutHistoryItem = (payload, histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.put(ApiPath, payload, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteHistoryItem = (histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.delete(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
