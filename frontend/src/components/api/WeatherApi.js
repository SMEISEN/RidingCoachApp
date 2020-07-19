/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetWeatherForecast = (pos) => new Promise((resolve, reject) => {
  const ApiPath = 'https://api.openweathermap.org/data/2.5/onecall?'
    + `lat=${pos.coords.latitude}&`
    + `lon=${pos.coords.longitude}&`
    + 'exclude=minutely,daily&'
    + `appid=${process.env.VUE_APP_OPENWEATHERMAP_API_KEY}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res.data))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetWeatherHistoric = (pos) => new Promise((resolve, reject) => {
  const ApiPath = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?'
    + `lat=${pos.coords.latitude}&`
    + `lon=${pos.coords.longitude}&`
    + 'exclude=current,minutely,daily&'
    + `dt=${Math.round(new Date().setUTCHours(0, 0, 0, 0) / 1000)}&`
    + `appid=${process.env.VUE_APP_OPENWEATHERMAP_API_KEY}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res.data))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
