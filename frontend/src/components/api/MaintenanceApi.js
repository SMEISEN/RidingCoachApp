/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all maintenance items from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetMaintenance = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Queries maintenance items from the database.
 * @param {object} query, e.g.,
 * {
 *   bike_id: "...",
 *   category: "...",
 *   name: "...",
 *   interval_unit: "...",
 *   interval_type: "...",
 *   interval_amount: {
 *     values: [5,15],
 *     operators: [">=", "<"]  // possible: ==, <=, >=, <, >, !=
 *   }
 * }
 * @returns {promise} Promise with API answer
 */
export const apiQueryMaintenance = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new maintenance entry to the database.
 * @param {object} payload maintenance object
 * @returns {promise} Promise with API answer
 */
export const apiPostMaintenance = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific maintenance entry from the database.
 * @param {string} mtnId id of the maintenance entry
 * @returns {promise} Promise with API answer
 */
export const apiGetMaintenanceItem = (mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific maintenance entry in the database.
 * @param {string} mtnId id of the maintenance entry
 * @param {object} payload maintenance object
 * @returns {promise} Promise with API answer
 */
export const apiPutMaintenanceItem = (payload, mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific maintenance entry in the database.
 * @param {string} mtnId id of the maintenance entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteMaintenanceItem = (mtnId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/${mtnId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets all maintenance warnings, i.e., maintenance items where maintenance needs to be done.
 * @param {string} bikeId id of the selected bike
 * @returns {promise} Promise with API answer
 */
export const apiGetMaintenanceWarnings = (bikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/maintenance/warnings/${bikeId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
