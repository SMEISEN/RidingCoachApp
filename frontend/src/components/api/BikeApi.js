import axios from 'axios';


const getBike = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/bike';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
})


export const BikeApi = {
  getBike,
};
