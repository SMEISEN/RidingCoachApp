/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetTrainings = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiQueryTrainings = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training/query';
  axios.post(ApiPath, query)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostTraining = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutTrainingItem = (payload, trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
