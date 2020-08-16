/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetAllCoaches = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostCoach = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutCoach = (coachId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
