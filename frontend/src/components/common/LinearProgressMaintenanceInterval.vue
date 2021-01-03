<template>
  <v-progress-linear
    color="primary"
    background-color="accent"
    height="22"
    :value="interval_relative"
    rounded
  >
    <template v-slot="{ value }">
      <span class="white--text">
        {{ interval_absolute + ' ' + interval_unit }} /
        {{ value }} %
      </span>
    </template>
  </v-progress-linear>
</template>

<script>
export default {
  name: 'LinearProgressMaintenanceInterval',
  props: {
    intervalState: {
      type: Object,
      required: true,
    },
    intervalUnit: {
      type: String,
      required: true,
    },
    absoluteDigits: {
      type: Number,
      required: false,
      default: 1,
    },
    relativeDigits: {
      type: Number,
      required: false,
      default: 0,
    },
  },
  computed: {
    interval_absolute() {
      return this.intervalState.absolute.toFixed(this.absoluteDigits);
    },
    interval_relative() {
      return (this.intervalState.relative * 100).toFixed(this.relativeDigits);
    },
    interval_unit() {
      return this.intervalUnit;
    },
  },
};
</script>

<style scoped>

</style>
