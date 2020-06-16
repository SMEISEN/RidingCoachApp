import axios from 'axios';


const getHistory = (query) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history/query';
  axios.post(ApiPath, query)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const postHistory = (payload) => new Promise((resolve, reject) => {
  const ApiPath = '/api/history';
  axios.post(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const getHistoryItem = (HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.get(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const putHistoryItem = (payload, HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.put(ApiPath, payload)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});
const deleteHistoryItem = (HistId) => new Promise((resolve, reject) => {
  const ApiPath = `/api/history/${HistId}`;
  axios.delete(ApiPath)
    .then((res) => resolve(res))
    .catch((error) => reject(console.error(error)));
});


export const HistoryApi = {
  getHistory,
  postHistory,
  getHistoryItem,
  putHistoryItem,
  deleteHistoryItem,
};
