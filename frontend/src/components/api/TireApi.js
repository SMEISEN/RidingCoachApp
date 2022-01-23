/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all tire entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetTire = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Queries tire entries from the database.
 * @param {object} query, e.g.,
 * {
 *   bike_id: "...",
 *   active: "...",
 *   category: "...",
 *   axis: "...",
 *   operating_hours: {
 *     values: [82,90],
 *     operators: [">=", "<"]  // possible: ==, <=, >=, <, >, !=
 *   },
 *   datetime_created: {
 *     ...
 *   },
 *  datetime_last_modified: {
 *     ...
 *   }
 * }
 * @returns {promise} Promise with API answer
 */
export const apiQueryTire = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new tire entry to the database.
 * @param {object} payload tire object
 * @returns {promise} Promise with API answer
 */
export const apiPostTire = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/tire';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific tire entry from the database.
 * @param {string} tireId id of the tire entry
 * @returns {promise} Promise with API answer
 */
export const apiGetTireItem = (tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific tire entry in the database.
 * @param {string} tireId id of the tire entry
 * @param {object} payload tire object
 * @returns {promise} Promise with API answer
 */
export const apiPutTireItem = (payload, tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific tire entry in the database.
 * @param {string} tireId id of the tire entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteTireItem = (tireId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/tire/${tireId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
