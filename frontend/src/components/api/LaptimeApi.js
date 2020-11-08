/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetLaptime = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/laptime';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetLaptimeItem = (laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutLaptimeItem = (payload, laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteLaptimeItem = (laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
