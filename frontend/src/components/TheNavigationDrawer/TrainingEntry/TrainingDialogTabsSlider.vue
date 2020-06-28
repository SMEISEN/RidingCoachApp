<template>
  <v-slider
    v-model="setup_entry.ticks_current"
    :tick-labels="tickLabels(setup_entry.ticks_standard, setup_entry.ticks_available)"
    :max="Number.parseInt(setup_entry.ticks_available)"
    step="1"
    ticks="always"
    append-icon="mdi-plus"
    prepend-icon="mdi-minus"
    @click:append="incrementSetup()"
    @click:prepend="decrementSetup()"
  >
  </v-slider>
</template>

<script>
export default {
  name: 'TrainingDialogTabsSlider',
  props: {
    setup_entry: {
      type: Object,
      required: true,
    },
  },
  methods: {
    incrementSetup() {
      this.setup_entry.ticks_current += 1;
      this.$forceUpdate();
    },
    decrementSetup() {
      this.setup_entry.ticks_current -= 1;
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
}
</script>

<style scoped>

</style>
