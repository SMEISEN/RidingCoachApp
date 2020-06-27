<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Suspension</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row dense>
        <v-col cols="12" xs="12" sm="3" md="2"
               v-for="(setup_entry, setup_index) in
               training_form_object.setup_individual[tab_item_index-1]"
               v-bind:key="setup_index"
        >
          <v-subheader>{{ setup_entry.name }}</v-subheader>
          <v-slider
            v-model="setup_entry.ticks_current"
            :tick-labels="tickLabels(setup_entry.ticks_standard, setup_entry.ticks_available)"
            :max="Number.parseInt(setup_entry.ticks_available)"
            step="1"
            ticks="always"
            append-icon="mdi-plus"
            prepend-icon="mdi-minus"
            @click:append=
              "incrementSetup(tab_item_index-1, setup_index)"
            @click:prepend=
              "decrementSetup(tab_item_index-1, setup_index)"
          >
          </v-slider>
        </v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: 'TrainingDialogTabsSetup',
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
  methods: {
    incrementSetup(tabIndex, setupIndex) {
      this.training_form_object.setup_individual[tabIndex][setupIndex].ticks_current += 1;
      this.$forceUpdate();
    },
    decrementSetup(tabIndex, setupIndex) {
      this.training_form_object.setup_individual[tabIndex][setupIndex].ticks_current -= 1;
      this.$forceUpdate();
    },
    tickLabels(standardTick, availableTicks) {
      const tick_labels = []
      for (let i = 0; i < availableTicks; i += 1) {
        if (i === Number.parseInt(standardTick)) {
          tick_labels.push('0');
        } else {
          tick_labels.push('');
        }
      }
      return tick_labels;
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
