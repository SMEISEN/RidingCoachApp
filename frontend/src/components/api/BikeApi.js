/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all bikes from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetAllBikes = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new bike to the database.
 * @param {object} payload bike object
 * @returns {promise} Promise with API answer
 */
export const apiPostBike = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific bike from the database.
 * @param {string} bikeId id of the bike
 * @returns {promise} Promise with API answer
 */
export const apiGetBike = (bikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific bike in the database.
 * @param {string} bikeId id of the bike
 * @param {object} payload bike object
 * @returns {promise} Promise with API answer
 */
export const apiPutBike = (bikeId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific bike in the database.
 * @param {string} bikeId id of the bike
 * @returns {promise} Promise with API answer
 */
export const apiDeleteBike = (bikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${bikeId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
