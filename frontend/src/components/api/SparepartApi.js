/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all spare part entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetSpareparts = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Queries spare part entries from the database.
 * @param {object} query, e.g.,
 * {
 *   bike_id: "...",
 *   name: "...",
 *   module: "...",
 *   min_stock: {
 *     values: [2,10],
 *     operators: [">=", "<"]  // possible: ==, <=, >=, <, >, !=
 *   }
 * }
 * @returns {promise} Promise with API answer
 */
export const apiQuerySpareparts = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart/query';
  axios.post(ApiPath, query, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new spare part entry to the database.
 * @param {object} payload spare part object
 * @returns {promise} Promise with API answer
 */
export const apiPostSparepart = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific spare part entry from the database.
 * @param {string} sparepartId id of the spare part entry
 * @returns {promise} Promise with API answer
 */
export const apiGetSparepartItem = (sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific spare part entry in the database.
 * @param {string} sparepartId id of the spare part entry
 * @param {object} payload spare part object
 * @returns {promise} Promise with API answer
 */
export const apiPutSparepartItem = (payload, sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific spare part entry in the database.
 * @param {string} sparepartId id of the spare part entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteSparepartItem = (sparepartId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/sparepart/${sparepartId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets all spare part warnings, i.e., spare parts where the current stock is lower than the minimal
 * stock.
 * @returns {promise} Promise with API answer
 */
export const apiGetSparepartWarnings = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepart/warnings';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
