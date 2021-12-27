/* eslint-disable import/prefer-default-export */
import axios from 'axios';
import querystring from 'query-string';
import moment from 'moment'

export const apiGetWeather = (pos) => new Promise((resolve, reject) => {
  const getTimelineURL = "https://api.tomorrow.io/v4/timelines";
  const apikey = process.env.VUE_APP_TOMORROWIO_API_KEY;
  let location = [pos.coords.latitude, pos.coords.longitude];
  const fields = [
    "precipitationIntensity",
    "humidity",
    "windSpeed",
    "temperature",
    "cloudCover",
    "weatherCode",
  ];
  const units = "metric";
  const timesteps = ["current", "1h"];
  const startTime =  moment.utc().subtract(6, "hours").toISOString();  // max 6 hours back
  const endTime = moment.utc().add(1, "days").startOf("day").toISOString();
  const getTimelineParameters =  querystring.stringify({
    apikey,
    location,
    fields,
    units,
    timesteps,
    startTime,
    endTime,
  }, {arrayFormat: "comma"});
  const ApiPath = getTimelineURL + "?" + getTimelineParameters;
  axios.get(ApiPath)
    .then((res) => resolve(res.data))
    .catch((error) => {
      console.error(error);
      reject(error);
    });
});
