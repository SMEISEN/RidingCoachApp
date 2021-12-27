/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all session entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetSession = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/session';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific session entry from the database.
 * @param {string} sessionId id of the session
 * @returns {promise} Promise with API answer
 */
export const apiGetSessionItem = (sessionId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/session/${sessionId}`;
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Modifies a specific session entry in the database.
 * @param {string} sessionId id of the session entry
 * @param {object} payload session object
 * @returns {promise} Promise with API answer
 */
export const apiPutSessionItem = (payload, sessionId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/session/${sessionId}`;
  axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Deletes a specific session entry in the database.
 * @param {string} sessionId id of the session entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteSessionItem = (sessionId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/session/${sessionId}`;
  axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
