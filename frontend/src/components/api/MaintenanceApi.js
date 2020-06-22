import axios from 'axios'


const getMaintenance = () => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance';
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const queryMaintenance = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/maintenance/query';
  axios.post(ApiPath, query)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});


export const MaintenanceApi = {
  getMaintenance,
  queryMaintenance,
};
