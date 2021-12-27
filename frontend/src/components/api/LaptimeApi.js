/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Gets all lap time entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetLaptime = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/laptime';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific lap time from the database.
 * @param {string} laptimeId id of the lap time
 * @returns {promise} Promise with API answer
 */
export const apiGetLaptimeItem = (laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific lap time entry in the database
 * @param {object} payload lap time object
 * @param {string} laptimeId id of the lap time entry
 * @returns {promise} Promise with API answer
 */
export const apiPutLaptimeItem = (payload, laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific lap time entry in the database.
 * @param {string} laptimeId id of the lap time entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteLaptimeItem = (laptimeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/laptime/${laptimeId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
