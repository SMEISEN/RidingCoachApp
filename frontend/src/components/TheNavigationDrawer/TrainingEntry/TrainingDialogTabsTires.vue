<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Tires</v-expansion-panel-header>
    <v-expansion-panel-content>
      <br>
      <v-window
        v-model="rain_tires"
      >
        <v-window-item>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-text-field
                v-model.number="trainingFormObject.setup_fixed[tabItemIndex].slick_pressure_front"
                label="Front tire pressure"
                suffix="bar"
                :hint="tire_pressure_recommendation.slick_front"
                persistent-hint
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureFront(tabItemIndex)"
                @click:prepend="decrementTirePressureFront(tabItemIndex)"
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-text-field
                v-model.number="trainingFormObject.setup_fixed[tabItemIndex].slick_pressure_rear"
                label="Rear tire pressure"
                suffix="bar"
                :hint="tire_pressure_recommendation.slick_rear"
                persistent-hint
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureRear(tabItemIndex)"
                @click:prepend="decrementTirePressureRear(tabItemIndex)"
              />
            </v-col>
          </v-row>
        </v-window-item>
        <v-window-item>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-text-field
                v-model.number="trainingFormObject.setup_fixed[tabItemIndex].rain_pressure_front"
                label="Front tire pressure"
                suffix="bar"
                :hint="tire_pressure_recommendation.rain_front"
                persistent-hint
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureFront(tabItemIndex)"
                @click:prepend="decrementTirePressureFront(tabItemIndex)"
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-text-field
                v-model.number="trainingFormObject.setup_fixed[tabItemIndex].rain_pressure_rear"
                label="Rear tire pressure"
                suffix="bar"
                :hint="tire_pressure_recommendation.rain_rear"
                persistent-hint
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureRear(tabItemIndex)"
                @click:prepend="decrementTirePressureRear(tabItemIndex)"
              />
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
      <br>
      <v-divider />
      <v-card-actions class="px-12 pt-6">
        <v-btn
          :disabled="rain_tires === 0"
          color="primary"
          @click="rain_tires--"
        >
          Slick
        </v-btn>
        <v-spacer />
        <v-btn
          :disabled="rain_tires === 1"
          color="primary"
          @click="rain_tires++"
        >
          Rain
        </v-btn>
      </v-card-actions>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import {
  incrementNumber,
  decrementNumber,
} from '../../utils/FromUtils';
import { interpolateLinearly1D } from '../../utils/DataProcessingUtils';
import { apiGetLocation } from '../../api/LocationApi';
import { apiGetWeather } from '../../api/WeatherApi';
import {
  calculateTrackSurfaceTemperatureDegCHassan2004
} from '../../common/TrackSufraceTemperatureModel';

export default {
  name: 'TrainingDialogTabsTires',
  props: {
    tabItemIndex: {
      type: Number,
      required: true,
    },
    trainingFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    rain_tires: 0,
    tire_pressure_recommendation: {
      slick_front: null,
      slick_rear: null,
      rain_front: null,
      rain_rear: null,
    },
    location_object: null,
  }),
  computed: {
    current_temperature_track_deg_c: {
      get() {
        return this.$store.getters.getCurrentTemperatureTrackDegC;
      },
      set(value) {
        this.$store.commit('setCurrentTemperatureTrackDegC', value);
      },
    },
    current_temperature_air_deg_c: {
      get() {
        return this.$store.getters.getCurrentTemperatureAirDegC;
      },
      set(value) {
        this.$store.commit('setCurrentTemperatureAirDegC', value);
      },
    },
    slick_front_pressure() {
      const slickTemperaturePressure = this.$store.getters.getCurrentBikeSlickFrontPressure;
      if (slickTemperaturePressure && slickTemperaturePressure.length > 0) {
        const arrayTemperaturePressure = slickTemperaturePressure.map(
          (x) => [x.temperature, x.pressure],
        );
        return interpolateLinearly1D(
          this.current_temperature_track_deg_c, arrayTemperaturePressure,
        );
      }
      return null;
    },
    slick_rear_pressure() {
      const slickTemperaturePressure = this.$store.getters.getCurrentBikeSlickRearPressure;
      if (slickTemperaturePressure && slickTemperaturePressure.length > 0) {
        const arrayTemperaturePressure = slickTemperaturePressure.map(
          (x) => [x.temperature, x.pressure],
        );
        return interpolateLinearly1D(
          this.current_temperature_track_deg_c, arrayTemperaturePressure,
        );
      }
      return null;
    },
    rain_front_pressure() {
      const slickTemperaturePressure = this.$store.getters.getCurrentBikeRainFrontPressure;
      if (slickTemperaturePressure && slickTemperaturePressure.length > 0) {
        const arrayTemperaturePressure = slickTemperaturePressure.map(
          (x) => [x.temperature, x.pressure],
        );
        return interpolateLinearly1D(
          this.current_temperature_track_deg_c, arrayTemperaturePressure,
        );
      }
      return null;
    },
    rain_rear_pressure() {
      const slickTemperaturePressure = this.$store.getters.getCurrentBikeRainRearPressure;
      if (slickTemperaturePressure && slickTemperaturePressure.length > 0) {
        const arrayTemperaturePressure = slickTemperaturePressure.map(
          (x) => [x.temperature, x.pressure],
        );
        return interpolateLinearly1D(
          this.current_temperature_track_deg_c, arrayTemperaturePressure,
        );
      }
      return null;
    },
  },
  watch: {
    rain_tires() {
      if (this.rain_tires === 0) {
        this.trainingFormObject.setup_fixed[this.tabItemIndex].rain_pressure_front = null;
        this.trainingFormObject.setup_fixed[this.tabItemIndex].rain_pressure_rear = null;
      } else {
        this.trainingFormObject.setup_fixed[this.tabItemIndex].slick_pressure_front = null;
        this.trainingFormObject.setup_fixed[this.tabItemIndex].slick_pressure_rear = null;
      }
    },
  },
  created() {
    this.getLocation().then(() => {
      this.getCurrentWeather().then(() => {
        this.getRecommendedTirePressure();
      });
    });
  },
  methods: {
    /**
     * Gets the location from the browser.
     * @returns {promise} Promise with API answer
     */
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
    /**
     * Gets the current weather information for the geolocation.
     * @returns {promise} Promise with API answer
     */
    getCurrentWeather() {
      return new Promise((resolve, reject) => {
        apiGetWeather(this.location_object)
          .then((res) => {
            this.current_temperature_air_deg_c = res.data.
              timelines[0].intervals[0].values.temperature;
            this.current_temperature_track_deg_c = calculateTrackSurfaceTemperatureDegCHassan2004(
              this.current_temperature_air_deg_c);
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
    /**
     * Depending on the temperature, recommend the optimal tire pressure.
     */
    getRecommendedTirePressure() {
      if (this.slick_front_pressure !== null) {
        this.tire_pressure_recommendation
          .slick_front = `recommended: ${this.slick_front_pressure.toFixed(2)} bar`;
      } else {
        this.tire_pressure_recommendation.slick_front = '';
      }
      if (this.slick_rear_pressure !== null) {
        this.tire_pressure_recommendation
          .slick_rear = `recommended: ${this.slick_rear_pressure.toFixed(2)} bar`;
      } else {
        this.tire_pressure_recommendation.slick_rear = '';
      }
      if (this.rain_front_pressure !== null) {
        this.tire_pressure_recommendation
          .rain_front = `recommended: ${this.rain_front_pressure.toFixed(2)} bar`;
      } else {
        this.tire_pressure_recommendation.rain_front = '';
      }
      if (this.rain_rear_pressure !== null) {
        this.tire_pressure_recommendation
          .rain_rear = `recommended: ${this.rain_rear_pressure.toFixed(2)} bar`;
      } else {
        this.tire_pressure_recommendation.rain_rear = '';
      }
    },
    /**
     * Increases the pressure of the front tire by 0.1 bar.
     * @param {number} ind index of the active setup tab
     */
    incrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.trainingFormObject.setup_fixed[ind].slick_pressure_front = incrementNumber(
          this.trainingFormObject.setup_fixed[ind].slick_pressure_front, 0.1, 1,
        );
      } else {
        this.trainingFormObject.setup_fixed[ind].rain_pressure_front = incrementNumber(
          this.trainingFormObject.setup_fixed[ind].rain_pressure_front, 0.1, 1,
        );
      }
    },
    /**
     * Decreases the pressure of the front tire by 0.1 bar.
     * @param {number} ind index of the active setup tab
     */
    decrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.trainingFormObject.setup_fixed[ind].slick_pressure_front = decrementNumber(
          this.trainingFormObject.setup_fixed[ind].slick_pressure_front, 0.1, 1,
        );
      } else {
        this.trainingFormObject.setup_fixed[ind].rain_pressure_front = decrementNumber(
          this.trainingFormObject.setup_fixed[ind].rain_pressure_front, 0.1, 1,
        );
      }
    },
    /**
     * Increases the pressure of the rear tire by 0.1 bar.
     * @param {number} ind index of the active setup tab
     */
    incrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.trainingFormObject.setup_fixed[ind].slick_pressure_rear = incrementNumber(
          this.trainingFormObject.setup_fixed[ind].slick_pressure_rear, 0.1, 1,
        );
      } else {
        this.trainingFormObject.setup_fixed[ind].rain_pressure_rear = incrementNumber(
          this.trainingFormObject.setup_fixed[ind].rain_pressure_rear, 0.1, 1,
        );
      }
    },
    /**
     * Decreases the pressure of the rear tire by 0.1 bar.
     * @param {number} ind index of the active setup tab
     */
    decrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.trainingFormObject.setup_fixed[ind].slick_pressure_rear = decrementNumber(
          this.trainingFormObject.setup_fixed[ind].slick_pressure_rear, 0.1, 1,
        );
      } else {
        this.trainingFormObject.setup_fixed[ind].rain_pressure_rear = decrementNumber(
          this.trainingFormObject.setup_fixed[ind].rain_pressure_rear, 0.1, 1,
        );
      }
    },
  },
};
</script>
