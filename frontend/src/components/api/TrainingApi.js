/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetTrainings = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQueryTrainings = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostTraining = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutTrainingItem = (payload, trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
