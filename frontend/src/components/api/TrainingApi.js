/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all training entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetTrainings = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Queries training entries from the database.
 * @param {object} query, e.g.,
 * {
 *   location: "...",
 *   datetime_created: {
 *     values: [utcSeconds,utcSeconds],
 *     operators: [">=", "<"]  // possible: ==, <=, >=, <, >, !=
 *   },
 *   datetime_last_modified: {
 *     ...
 *   },
 *  datetime_display: {
 *     ...
 *   }
 * }
 * @returns {promise} Promise with API answer
 */
export const apiQueryTrainings = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new training entry to the database.
 * @param {object} payload training object
 * @returns {promise} Promise with API answer
 */
export const apiPostTraining = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/training';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific training entry from the database.
 * @param {string} trainingId id of the training entry
 * @returns {promise} Promise with API answer
 */
export const apiGetTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific training entry in the database.
 * @param {string} trainingId id of the training entry
 * @param {object} payload training object
 * @returns {promise} Promise with API answer
 */
export const apiPutTrainingItem = (payload, trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific training entry in the database.
 * @param {string} trainingId id of the training entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteTrainingItem = (trainingId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/training/${trainingId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
