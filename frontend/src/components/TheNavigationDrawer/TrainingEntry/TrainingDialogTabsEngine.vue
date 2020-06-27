<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Engine</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row dense align="start">
        <v-col cols="11" xs="0" sm="1" md="1"></v-col>
        <v-col cols="11" xs="11" sm="4" md="4">
          <v-subheader>Operating hours*</v-subheader>
          <v-text-field
            dense
            append-outer-icon="mdi-plus"
            prepend-icon="mdi-minus"
            @click:append-outer="incrementHour(tab_item_index-1)"
            @click:prepend="decrementHour(tab_item_index-1)"
            :rules="[v => !!v]"
            required
            suffix="h"
            v-model="training_form_object.setup_fixed[tab_item_index-1].operating_hours">
          </v-text-field>
        </v-col>
        <v-col cols="11" xs="0" sm="1" md="1"></v-col>
        <v-col cols="11" xs="11" sm="4" md="4">
          <v-subheader>Mode*</v-subheader>
          <hr style="height:3pt; visibility:hidden;" />
          <v-slider
            v-model="engine_mode"
            :tick-labels="['soft','performance']"
            :min="1"
            :max="2"
            step="1"
            ticks="always"
            tick-size="4"
            append-icon="mdi-plus"
            prepend-icon="mdi-minus"
          >
          </v-slider>
        </v-col>
        <v-col cols="11" xs="0" sm="1" md="1"></v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import {FormUtils} from '../../utils/FromUtils';

export default {
  name: 'TrainingDialogTabsEngine',
  props: {
    tab_item_index: {
      type: Number,
      required:true,
    },
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    engine_mode: null,
  }),
  methods: {
    incrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.incrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1)
    },
    decrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.decrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1)
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
