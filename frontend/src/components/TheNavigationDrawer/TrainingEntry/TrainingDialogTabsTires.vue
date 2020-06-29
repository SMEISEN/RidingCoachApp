<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Tires</v-expansion-panel-header>
    <v-expansion-panel-content>
      <br/>
      <v-window
        v-model="rain_tires"
      >
        <v-window-item>
          <v-row dense>
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16">
              <v-text-field
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureFront(tab_item_index)"
                @click:prepend="decrementTirePressureFront(tab_item_index)"
                :rules="[v => !!v]"
                required
                label="Front tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
                persistent-hint
                v-model="training_form_object.setup_fixed[tab_item_index].slick_pressure_front">
              </v-text-field>
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16">
              <v-text-field
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer=
                  "incrementTirePressureRear(tab_item_index)"
                @click:prepend=
                  "decrementTirePressureRear(tab_item_index)"
                :rules="[v => !!v]"
                required
                label="Rear tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
                persistent-hint
                v-model="training_form_object.setup_fixed[tab_item_index].slick_pressure_rear">
              </v-text-field>
            </v-col>
          </v-row>
        </v-window-item>
        <v-window-item>
          <v-row dense>
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16">
              <v-text-field
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureFront(tab_item_index)"
                @click:prepend="decrementTirePressureFront(tab_item_index)"
                :rules="[v => !!v]"
                required
                label="Front tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
                persistent-hint
                v-model="training_form_object.setup_fixed[tab_item_index].rain_pressure_front">
              </v-text-field>
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16">
              <v-text-field
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementTirePressureRear(tab_item_index)"
                @click:prepend="decrementTirePressureRear(tab_item_index)"
                :rules="[v => !!v]"
                required
                label="Rear tire pressure"
                suffix="bar"
                hint="recommended: 2.1 bar"
                persistent-hint
                v-model=
                  "training_form_object.setup_fixed[tab_item_index].rain_pressure_rear">
              </v-text-field>
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
      <br/>
      <v-divider></v-divider>
      <v-card-actions  class="px-12 pt-6">
        <v-btn
          :disabled="rain_tires === 0"
          color="primary"
          @click="rain_tires--"
        >
          Slick
        </v-btn>
        <v-spacer></v-spacer>
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
import {FormUtils} from '../../utils/FromUtils';

export default {
  name: 'TrainingDialogTabsTires',
  props: {
    tab_item_index: {
      type: Number,
      required: true,
    },
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    rain_tires: 0,
  }),
  methods: {
    incrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_front =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_front, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_front =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_front, 0.1, 1)
      }
    },
    decrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_front =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_front, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_front =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_front, 0.1, 1)
      }
    },
    incrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_rear =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_rear, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_rear =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_rear, 0.1, 1)
      }
    },
    decrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_rear =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_rear, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_rear =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_rear, 0.1, 1)
      }
    },
  },
  updated() {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
