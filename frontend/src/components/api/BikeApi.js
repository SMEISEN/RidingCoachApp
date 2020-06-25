import axios from 'axios';


const getBike = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const postBikeData = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const putBike = (BikeId, payload) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${BikeId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const deleteBike = (BikeId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/bike/${BikeId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});


export const BikeApi = {
  getBike,
  postBikeData,
  putBike,
  deleteBike,
};
