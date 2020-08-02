/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetAllBikes = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostBike = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetBike = (bikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPutBike = (bikeId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiDeleteBike = (bikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
