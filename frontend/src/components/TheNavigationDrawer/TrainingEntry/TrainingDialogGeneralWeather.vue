<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Weather</v-expansion-panel-header>
    <v-expansion-panel-content>
      <LineChart
        v-if="data_processed === true"
        :chart-data="data_collection"
        :options="data_options"
        :height="null"
        :width="null"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import moment from 'moment-timezone';
import { apiGetWeatherForecast, apiGetWeatherHistoric } from '../../api/WeatherApi';
import { apiGetLocation } from '../../api/LocationApi';
import LineChart from '../../common/LineChart.vue';

export default {
  name: 'TrainingDialogGeneralWeather',
  components: {
    LineChart,
  },
  props: {
    trainingFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    weather_array: [],
    time_array: [],
    data_collection: {
      labels: [],
      datasets: [],
    },
    data_sets: [
      {
        label: 'Air temperature',
        data: [],
        backgroundColor: 'transparent',
        borderColor: '',
        pointBackgroundColor: '',
      },
      {
        label: 'Track surface temperature',
        data: [],
        backgroundColor: 'transparent',
        borderColor: '',
        pointBackgroundColor: '',
      },
    ],
    data_options: {
      responsive: true,
      aspectRatio: 2,
      maintainAspectRatio: true,
      title: {
        display: false,
        text: 'Weather Data',
      },
      legend: {
        labels: {
          boxWidth: 10,
          fontSize: 10,
        },
      },
      scales: {
        xAxes: [
          {
            type: 'time',
            distribution: 'linear',
            ticks: {
              source: 'labels',
              fontSize: 10,
              callback(value) {
                if (value.slice(-9) !== '00:00:000') {
                  return '';
                }
                return value.replace(value.slice(-7), '');
              },
            },
            time: {
              unit: 'millisecond',
              displayFormats: {
                millisecond: 'HH:mm:ss:SSS',
              },
            },
            gridLines: {
              color: [],
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              fontSize: 10,
            },
          },
        ],
      },
    },
    data_processed: false,
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
        const hourTo = 19 + utcOffset;
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
            this.trainingFormObject.weather = weatherMeasurement.concat(weatherMeasurement);
            this.trainingFormObject.setup_fixed[this.tabItemIndex]
              .weather_current = resForecast.current;
            weatherForecast.unshift(resForecast.current);
            for (let i = 0; i < weatherForecast.length; i += 1) {
              Object.assign(
                weatherForecast[i],
                { type: 'forecast' },
              );
            }
            this.weather_array = weatherMeasurement.concat(weatherForecast);
            this.extractTemperature(weatherMeasurement.length);
          });
        } else {
          this.weather_array = weatherMeasurement;
          this.extractTemperature(weatherMeasurement.length);
        }
      });
    },
    extractTemperature(currentTick) {
      this.data_sets[0].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[0].borderColor = this.$vuetify.theme.themes.light.accent;
      this.data_sets[1].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[1].borderColor = this.$vuetify.theme.themes.light.error;
      for (let i = 0; i < this.weather_array.length; i += 1) {
        const airDegrees = this.weather_array[i].temp - 273.15;
        this.data_sets[0].data.push(airDegrees);
        this.data_sets[1].data.push(1.52 * airDegrees - 4.4436);
        if (i === currentTick) {
          this.data_options.scales.xAxes[0].gridLines.color
            .push(this.$vuetify.theme.themes.light.info);
        } else {
          this.data_options.scales.xAxes[0].gridLines.color
            .push('rgba(0, 0, 0, 0.1)');
        }
        this.time_array.push(new Date(this.weather_array[i].dt * 1000));
      }
      this.data_collection.datasets = this.data_sets;
      this.data_collection.labels = this.time_array;
      this.data_processed = true;
    },
  },
};
</script>

<style scoped>

</style>
