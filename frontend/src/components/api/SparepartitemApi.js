/* eslint-disable import/prefer-default-export */
import axios from 'axios';

/**
 * Get all spare part item entries from the database.
 * @returns {promise} Promise with API answer
 */
export const apiGetSparepartitems = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepartitem';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Posts a new spare part item entry to the database.
 * @param {object} payload spare part item object
 * @returns {promise} Promise with API answer
 */
export const apiPostSparepartitem = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepartitem';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
/**
 * Gets a specific spare part item entry from the database.
 * @param {string} sparepartitemId id of the spare part item entry
 * @returns {promise} Promise with API answer
 */
export const apiGetSparepartitemItem = (sparepartitemId) => new Promise(
  (resolve, reject) => {
    const ApiPath = `/api/sparepartitem/${sparepartitemId}`;
    axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
      .then((res) => resolve(res))
      .catch((error) => {
        console.error(error);
        reject(error);
      });
  },
);
/**
 * Modifies a specific spare part item entry in the database.
 * @param {string} sparepartitemId id of the spare part item entry
 * @param {object} payload spare part item object
 * @returns {promise} Promise with API answer
 */
export const apiPutSparepartitemItem = (payload, sparepartitemId) => new Promise(
  (resolve, reject) => {
    const ApiPath = `/api/sparepartitem/${sparepartitemId}`;
    axios.put(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
      .then((res) => resolve(res))
      .catch((error) => {
        console.error(error);
        reject(error);
      });
  },
);
/**
 * Deletes a specific spare part item entry in the database.
 * @param {string} sparepartitemId id of the spare part item entry
 * @returns {promise} Promise with API answer
 */
export const apiDeleteSparepartitemItem = (sparepartitemId) => new Promise(
  (resolve, reject) => {
    const ApiPath = `/api/sparepartitem/${sparepartitemId}`;
    axios.delete(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
      .then((res) => resolve(res))
      .catch((error) => {
        console.error(error);
        reject(error);
      });
  },
);
