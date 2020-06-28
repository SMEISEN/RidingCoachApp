<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Electronic</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row dense>
        <v-col cols="12" xs="12" sm="3" md="2"
               v-for="(setup_entry, setup_index) in electronic_setup"
               v-bind:key="setup_index"
        >
          <v-subheader>{{ setup_entry.name }}</v-subheader>
          <TrainingDialogTabsSlider
            :setup_entry="setup_entry"
          />
        </v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider';

export default {
  name: 'TrainingDialogTabsElectronic',
  components: {
    TrainingDialogTabsSlider,
  },
  props: {
    tab_item_index: {
      type: Number,
      required: true,
    },
    training_form_object: {
      type: Object,
      required:true,
    },
  },
  computed: {
    electronic_setup() {
      return this.training_form_object.setup_individual[this.tab_item_index]
        .filter(i => i.category === 'Electronic');
    },
  },
}
</script>

<style scoped>

</style>
