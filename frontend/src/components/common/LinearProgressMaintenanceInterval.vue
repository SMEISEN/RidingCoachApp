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
    absoluteDigitstoPrecision: {
      type: Number,
      required: false,
      default: 2,
    },
    relativeDigitsToFixed: {
      type: Number,
      required: false,
      default: 0,
    },
  },
  computed: {
    interval_absolute() {
      return this.intervalState.absolute.toPrecision(this.absoluteDigitstoPrecision);
    },
    interval_relative() {
      return (this.intervalState.relative * 100).toFixed(this.relativeDigitsToFixed);
    },
    interval_unit() {
      return this.intervalUnit;
    },
  },
};
</script>
