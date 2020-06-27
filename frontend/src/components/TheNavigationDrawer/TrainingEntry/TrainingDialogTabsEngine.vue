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
        <v-col cols="11" xs="11" sm="4" md="4"
               v-for="(setup_entry, setup_index) in engine_setup"
               v-bind:key="setup_index"
        >
          <v-subheader>{{ setup_entry.name }}</v-subheader>
          <hr style="height:3pt; visibility:hidden;" />
          <TrainingDialogTabsSlider
            :tab_item_index="tab_item_index"
            :setup_entry="setup_entry"
            :training_form_object="training_form_object"
          />
        </v-col>
        <v-col cols="11" xs="0" sm="1" md="1"></v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import {FormUtils} from '../../utils/FromUtils';
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider';

export default {
  name: 'TrainingDialogTabsEngine',
  components: {
    TrainingDialogTabsSlider,
  },
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
  computed: {
    engine_setup() {
      return this.training_form_object.setup_individual[this.tab_item_index -1]
        .filter(i => i.category === 'Engine');
    },
  },
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
