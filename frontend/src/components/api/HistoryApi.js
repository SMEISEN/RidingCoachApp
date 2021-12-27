/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all maintenance history entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetHistory = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Queries maintenance history entries from the database.
 * @param {object} query, e.g.,
 * {
 *   bike_id: "...",
 *   comment: "...",
 *   operating_hours: {
 *     values: [82,90],
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
export const apiQueryHistory = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new maintenance history entry to the database.
 * @param {object} payload maintenance history object
 * @returns {promise} Promise with API answer
 */
export const apiPostHistory = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific maintenance history entry from the database.
 * @param {string} histId id of the maintenance history entry
 * @returns {promise} Promise with API answer
 */
export const apiGetHistoryItem = (histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific maintenance history entry in the database.
 * @param {string} histId id of the maintenance history entry
 * @param {object} payload maintenance history object
 * @returns {promise} Promise with API answer
 */
export const apiPutHistoryItem = (payload, histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific maintenance history entry in the database.
 * @param {string} histId id of the maintenance history entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteHistoryItem = (histId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${histId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
