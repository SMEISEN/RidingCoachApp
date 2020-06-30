/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetHistory = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history/query';
  axios.post(ApiPath, query)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPostHistory = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiGetHistoryItem = (HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPutHistoryItem = (payload, HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiDeleteHistoryItem = (HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
