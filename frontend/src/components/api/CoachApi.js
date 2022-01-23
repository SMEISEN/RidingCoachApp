/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all coach items from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetAllCoaches = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new coach item to the database.
 * @param {object} payload coach object
 * @returns {promise} Promise with API answer
 */
export const apiPostCoach = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/coach';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific coach item from the database.
 * @param {string} coachId id of the coach item
 * @returns {promise} Promise with API answer
 */
export const apiGetCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific coach item in the database.
 * @param {string} coachId id of the coach item
 * @param {object} payload coach object
 * @returns {promise} Promise with API answer
 */
export const apiPutCoach = (coachId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific coach item in the database.
 * @param {string} coachId id of the coach item
 * @returns {promise} Promise with API answer
 */
export const apiDeleteCoach = (coachId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/coach/${coachId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
