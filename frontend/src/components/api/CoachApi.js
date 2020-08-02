/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetAllCoaches = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostCoach = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutCoach = (coachId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
