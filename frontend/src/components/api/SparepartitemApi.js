/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetSparepartitems = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepartitem';
  axios.get(ApiPath, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiPostSparepartitem = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/sparepartitem';
  axios.post(ApiPath, payload, { headers: { apikey: process.env.VUE_APP_RESTPLUS_API_KEY } })
    .then((res) => resolve(res))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
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
