<template>
  <v-slider
    v-model.number="setupEntry.ticks_current"
    :tick-labels="tickLabels(setupEntry.ticks_standard, setupEntry.ticks_available)"
    :max="Number.parseInt(setupEntry.ticks_available)"
    step="1"
    ticks="always"
    tick-size="3"
    thumb-size="18"
    :thumb-label="true"
    append-icon="mdi-plus"
    prepend-icon="mdi-minus"
    @click:append="incrementSetup()"
    @click:prepend="decrementSetup()"
  />
</template>

<script>
export default {
  name: 'TrainingDialogTabsSlider',
  props: {
    setupEntry: {
      type: Object,
      required: true,
    },
  },
  methods: {
    incrementSetup() {
      this.setupEntry.ticks_current += 1;
      this.$forceUpdate();
    },
    decrementSetup() {
      this.setupEntry.ticks_current -= 1;
      this.$forceUpdate();
    },
    tickLabels(standardTick, availableTicks) {
      const tickLabels = [];
      for (let i = 0; i < availableTicks; i += 1) {
        if (i === Number.parseInt(standardTick, 10)) {
          tickLabels.push('I');
        } else {
          tickLabels.push('');
        }
      }
      return tickLabels;
    },
  },
};
</script>

<style scoped>

</style>
