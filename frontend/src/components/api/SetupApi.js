/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all setup entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetSetups = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new setup entry to the database.
 * @param {object} payload setup object
 * @returns {promise} Promise with API answer
 */
export const apiPostSetup = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/setup';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific setup entry from the database.
 * @param {string} setupId id of the setup entry
 * @returns {promise} Promise with API answer
 */
export const apiGetSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific setup entry in the database.
 * @param {string} setupId id of the setup entry
 * @param {object} payload setup object
 * @returns {promise} Promise with API answer
 */
export const apiPutSetupItem = (payload, setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific setup entry in the database.
 * @param {string} setupId id of the setup entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteSetupItem = (setupId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/setup/${setupId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
