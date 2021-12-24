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
import { apiGetLocation } from '../../api/LocationApi';
import { apiGetWeather } from '../../api/WeatherApi';
import LineChart from '../../common/LineChart.vue';
import {
  calculateTrackSurfaceTemperatureDegCHassan2004
} from '../../common/TrackSufraceTemperatureModel';

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
        label: 'Track surface temperature [Hassan2004]',
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
      apiGetWeather(this.location_object)
        .then((res) => {
          const weather_current = res.data.timelines[0].intervals;
          const timestamp_current = res.data.timelines[0].startTime;
          const weather_past_future = res.data.timelines[1].intervals;
          this.extractTemperature(weather_past_future, weather_current, timestamp_current);
          this.trainingFormObject.weather = weather_past_future;
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    extractTemperature(weatherPastFuture, weatherCurrent, timestampCurrent) {
      this.data_sets[0].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[0].borderColor = this.$vuetify.theme.themes.light.accent;
      this.data_sets[1].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
      this.data_sets[1].borderColor = this.$vuetify.theme.themes.light.error;
      let timestampPreviousIteration = weatherPastFuture[0].startTime;
      let timeArray = []
      for (let i = 0; i < weatherPastFuture.length; i += 1) {
        const timestampCurrentIteration = weatherPastFuture[i].startTime;
        const airDegC = weatherPastFuture[i].values.temperature;
        const asphaltDegC = calculateTrackSurfaceTemperatureDegCHassan2004(airDegC);
        if (  // insert current time stamp
          timestampCurrent > timestampPreviousIteration &&
          timestampCurrent < timestampCurrentIteration) {
          const currentAirDegC = weatherCurrent[0].values.temperature;
          const currentAsphaltDegC = calculateTrackSurfaceTemperatureDegCHassan2004(currentAirDegC);
          this.$store.commit('setCurrentTemperatureAirDegC', currentAirDegC);
          this.$store.commit('setCurrentTemperatureTrackDegC', currentAsphaltDegC);
          timeArray.push(new Date(timestampCurrent));
          this.data_sets[0].data.push(currentAirDegC);
          this.data_sets[1].data.push(currentAsphaltDegC);
          this.data_options.scales.xAxes[0].gridLines.color.push(
            this.$vuetify.theme.themes.light.info);
        }
        timeArray.push(new Date(timestampCurrentIteration));
        this.data_sets[0].data.push(airDegC);
        this.data_sets[1].data.push(asphaltDegC);
        this.data_options.scales.xAxes[0].gridLines.color.push(
          'rgba(0, 0, 0, 0.1)');
        timestampPreviousIteration = timestampCurrentIteration;
      }
      this.data_collection.datasets = this.data_sets;
      this.data_collection.labels = timeArray;
      this.data_processed = true;
    },
  },
};
</script>

<style scoped>

</style>
