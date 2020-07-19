/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const apiGetWeatherForecast = (pos) => new Promise((resolve, reject) => {
  const ApiPath = 'https://api.climacell.co/v3/weather/forecast/hourly?'
    + `lat=${pos.coords.latitude}&`
    + `lon=${pos.coords.longitude}&`
    + 'unit_system=si&'
    + 'start_time=now&'
    + `end_time=${new Date(new Date().setUTCHours(24, 0, 0, 0)).toISOString()}&`
    + '&fields='
      + 'temp'
    + '%2C'
      + 'wind_speed'
    + '%2C'
      + 'surface_shortwave_radiation'
    + '%2C'
      + 'humidity'
    + '%2C'
      + 'precipitation_probability'
    + '%2C'
      + 'precipitation'
    + '%2C'
      + 'weather_code'
    + '%2C'
      + 'cloud_cover'
    + '&'
    + `apikey=${process.env.VUE_APP_CLIMACELL_API_KEY}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res.data))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
export const apiGetWeatherHistoric = (pos) => new Promise((resolve, reject) => {
  const ApiPath = 'https://api.climacell.co/v3/weather/historical/climacell?'
    + `lat=${pos.coords.latitude}&`
    + `lon=${pos.coords.longitude}&`
    + 'timestep=60&'
    + 'unit_system=si&'
    + `start_time=${new Date(new Date().setUTCHours(0, 0, 0, 0)).toISOString()}&`
    + 'end_time=now&'
    + 'fields='
      + 'temp'
    + '%2C'
      + 'wind_speed'
    + '%2C'
      + 'surface_shortwave_radiation'
    + '%2C'
      + 'humidity'
    + '%2C'
      + 'precipitation'
    + '%2C'
      + 'weather_code'
    + '%2C'
      + 'cloud_cover'
    + '&'
    + `apikey=${process.env.VUE_APP_CLIMACELL_API_KEY}`;
  axios.get(ApiPath, { timeout: 5000 })
    .then((res) => resolve(res.data))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
