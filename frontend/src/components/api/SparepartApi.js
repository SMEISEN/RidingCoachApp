/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetSpareparts = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQuerySpareparts = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostSparepart = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetSparepartItem = (sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutSparepartItem = (payload, sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteSparepartItem = (sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
