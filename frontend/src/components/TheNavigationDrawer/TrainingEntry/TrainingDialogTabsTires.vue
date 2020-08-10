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
  }),
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
  updated() {
  },
  created() {
    this.getRecommendedTirePressure();
  },
  methods: {
    getRecommendedTirePressure() {
      const slickFrontPressure = this.$store.getters.getCurrentBikeSlickFrontPressure;
      const slickRearPressure = this.$store.getters.getCurrentBikeSlickRearPressure;
      const rainFrontPressure = this.$store.getters.getCurrentBikeRainFrontPressure;
      const rainRearPressure = this.$store.getters.getCurrentBikeRainRearPressure;
      if (slickFrontPressure !== null) {
        this.tire_pressure_recommendation.slick_front = `recommended: ${slickFrontPressure} bar`;
      } else {
        this.tire_pressure_recommendation.slick_front = '';
      }
      if (slickRearPressure !== null) {
        this.tire_pressure_recommendation.slick_rear = `recommended: ${slickRearPressure} bar`;
      } else {
        this.tire_pressure_recommendation.slick_rear = '';
      }
      if (rainFrontPressure !== null) {
        this.tire_pressure_recommendation.rain_front = `recommended: ${rainFrontPressure} bar`;
      } else {
        this.tire_pressure_recommendation.rain_front = '';
      }
      if (rainRearPressure !== null) {
        this.tire_pressure_recommendation.rain_rear = `recommended: ${rainRearPressure} bar`;
      } else {
        this.tire_pressure_recommendation.rain_rear = '';
      }
    },
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

<style scoped>

</style>
