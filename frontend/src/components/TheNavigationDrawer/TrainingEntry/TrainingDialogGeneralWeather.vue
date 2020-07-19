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
  computed: {
    training_setup_tab() {
      return this.$store.getters.getTrainingDialogSetupActiveTab;
    },
  },
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
          .catch((error) => {
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
            reject(error);
          });
      });
    },
    getWeather() {
      apiGetWeatherHistoric(this.location_object)
        .then((resMeasurement) => {
          const timezone = moment.tz.guess();
          const utcOffset = moment.tz.zone(timezone).utcOffset(new Date().getTime()) / 60;
          const hourFrom = 8 + utcOffset;
          const hourTo = 19 + utcOffset;
          const weatherMeasurement = resMeasurement.slice(hourFrom, hourTo);
          for (let i = 0; i < weatherMeasurement.length; i += 1) {
            Object.assign(
              weatherMeasurement[i],
              { type: 'measurement' },
            );
          }
          [this.trainingFormObject.setup_fixed[this.training_setup_tab]
            .weather_current] = weatherMeasurement.slice(-1);
          const currentUtcHour = resMeasurement.length + 1 + utcOffset;
          if (hourTo - currentUtcHour > 0) {
            apiGetWeatherForecast(this.location_object)
              .then((resForecast) => {
                const weatherForecast = resForecast.slice(1, hourTo - currentUtcHour + 1);
                for (let i = 0; i < weatherForecast.length; i += 1) {
                  Object.assign(weatherForecast[i], { type: 'forecast' });
                }
                const weatherComplete = weatherMeasurement.concat(weatherForecast);
                this.weather_array = weatherComplete;
                this.trainingFormObject.weather = weatherComplete;
                this.extractTemperature(weatherMeasurement.length - 1);
              })
              .catch((error) => {
                this.$store.commit('setInfoSnackbar', {
                  state: true,
                  color: 'error',
                  message: `${error}!`,
                });
              });
          } else {
            this.weather_array = weatherMeasurement;
            this.trainingFormObject.weather = weatherMeasurement;
            this.extractTemperature(weatherMeasurement.length - 1);
          }
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    extractTemperature(currentTick) {
      this.data_sets[0].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[0].borderColor = this.$vuetify.theme.themes.light.accent;
      this.data_sets[1].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[1].borderColor = this.$vuetify.theme.themes.light.error;
      for (let i = 0; i < this.weather_array.length; i += 1) {
        const airDegrees = this.weather_array[i].temp.value;
        this.data_sets[0].data.push(airDegrees);
        if (airDegrees !== null) {
          const windSpeed = this.weather_array[i].wind_speed.value;
          const humidity = this.weather_array[i].humidity.value;
          const solarRadiation = this.weather_array[i].surface_shortwave_radiation.value;
          const asphaltFahrenheit = 41.51
            + 0.102 * windSpeed
            + 1.71 * airDegrees
            + 0.032 * humidity
            - 0.029 * solarRadiation
            + 0.002 * airDegrees * humidity
            + 5.7 * (10 ** -4) * windSpeed * solarRadiation
            + 0.0014 * solarRadiation
            + 4.09 * (10 ** -5) * (solarRadiation ** 2)
            - 1.15 * (10 ** -6) * airDegrees * (solarRadiation ** 2);
          const asphaltDegrees = (asphaltFahrenheit - 32) / 1.8;
          this.data_sets[1].data.push(asphaltDegrees);
        } else {
          this.data_sets[1].data.push(null);
        }
        if (i === currentTick) {
          this.data_options.scales.xAxes[0].gridLines.color
            .push(this.$vuetify.theme.themes.light.info);
        } else {
          this.data_options.scales.xAxes[0].gridLines.color
            .push('rgba(0, 0, 0, 0.1)');
        }
        this.time_array.push(new Date(this.weather_array[i].observation_time.value));
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
