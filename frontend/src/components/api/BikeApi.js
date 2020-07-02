/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetAllBikes = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPostBike = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiGetBike = (BikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${BikeId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiPutBike = (BikeId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${BikeId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
export const apiDeleteBike = (BikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${BikeId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
