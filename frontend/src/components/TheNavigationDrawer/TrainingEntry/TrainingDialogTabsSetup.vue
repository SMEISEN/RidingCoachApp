<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Suspension</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row dense>
        <v-col cols="12" xs="12" sm="3" md="2"
               v-for="(setup_entry, setup_index) in suspension_setup"
               :key="'tab-item/' + tab_item_index + '/setup-item/' + setup_index"
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
  name: 'TrainingDialogTabsSetup',
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
    suspension_setup() {
      return this.training_form_object.setup_individual[this.tab_item_index]
        .filter(i => i.category === 'Suspension');
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
