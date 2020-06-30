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
                v-model="trainingFormObject.setup_fixed[tabItemIndex].slick_pressure_front"
                :rules="[v => !!v]"
                required
                label="Front tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
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
                v-model="trainingFormObject.setup_fixed[tabItemIndex].slick_pressure_rear"
                :rules="[v => !!v]"
                required
                label="Rear tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
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
                v-model="trainingFormObject.setup_fixed[tabItemIndex].rain_pressure_front"
                :rules="[v => !!v]"
                required
                label="Front tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
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
                v-model="trainingFormObject.setup_fixed[tabItemIndex].rain_pressure_rear"
                :rules="[v => !!v]"
                required
                label="Rear tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
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
  }),
  updated() {
  },
  created() {
  },
  methods: {
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
