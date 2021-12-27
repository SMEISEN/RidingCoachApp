/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetTire = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQueryTire = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostTire = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetTireItem = (tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutTireItem = (payload, tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteTireItem = (tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
