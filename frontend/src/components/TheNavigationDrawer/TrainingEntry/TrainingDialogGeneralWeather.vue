<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Weather</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-sparkline
        :value="temperature_array"
        :labels="time_array"
        show-labels
        stroke-linecap="round"
        line-width="2"
        label-size="4"
        type="trend"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import moment from 'moment-timezone';
import { apiGetWeatherForecast, apiGetWeatherHistoric } from '../../api/WeatherApi';
import { apiGetLocation } from '../../api/LocationApi';

export default {
  name: 'TrainingDialogGeneralWeather',
  props: {
    trainingFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    weather_array: [],
    temperature_array: [],
    time_array: [],
  }),
  updated() {
  },
  created() {
    this.getGeneralProperties();
  },
  methods: {
    getGeneralProperties() {
      this.getLocation().then(() => {
        this.getWeather();
      });
    },
    getLocation() {
      return new Promise((resolve, reject) => {
        apiGetLocation()
          .then((res) => {
            this.location_object = res;
            resolve(res);
          })
          .catch((error) => reject(console.error(error)));
      });
    },
    getWeather() {
      apiGetWeatherHistoric(this.location_object).then((resMeasurement) => {
        const timezone = moment.tz.guess();
        const utcOffset = moment.tz.zone(timezone).utcOffset(new Date().getTime()) / 60;
        const hourFrom = 8 + utcOffset;
        const hourTo = 18 + utcOffset;
        const weatherMeasurement = resMeasurement.hourly.slice(hourFrom, hourTo);
        for (let i = 0; i < weatherMeasurement.length; i += 1) {
          Object.assign(
            weatherMeasurement[i],
            { type: 'measurement' },
          );
        }
        const currentUtcHour = resMeasurement.hourly.length + 1 + utcOffset;
        if (hourTo - currentUtcHour > 0) {
          apiGetWeatherForecast(this.location_object).then((resForecast) => {
            const weatherForecast = resForecast.hourly.slice(1, hourTo - currentUtcHour);
            for (let i = 0; i < weatherForecast.length; i += 1) {
              Object.assign(
                weatherForecast[i],
                { type: 'forecast' },
              );
            }
            this.weather_array = weatherMeasurement.concat(weatherForecast);
          });
        } else {
          this.weather_array = weatherMeasurement;
        }
        this.extractTemperature();
      });
    },
    extractTemperature() {
      for (let i = 0; i < this.weather_array.length; i += 1) {
        this.temperature_array.push(this.weather_array[i].temp - 273.15);
        this.time_array.push(new Date(this.weather_array[i].dt * 1000)
          .toTimeString().substr(0, 5));
      }
    },
  },
};
</script>

<style scoped>

</style>
