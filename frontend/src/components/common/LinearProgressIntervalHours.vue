<template>
  <v-progress-linear
    color="primary"
    background-color="accent"
    height="22"
    :value="currentStateIntervalHours()"
    rounded
  >
    <template v-slot="{ value }">
      <span class="white--text">
        {{ leftIntervalHours() }} h /
        {{ Math.ceil(value) }} %
      </span>
    </template>
  </v-progress-linear>
</template>

<script>
import {
  processStateOfIntervalHours,
  processLeftIntervalHours,
} from '../utils/DataProcessingUtils';

export default {
  name: 'LinearProgressIntervalHours',
  props: {
    hoursLatest: {
      type: Number,
      required: true,
    },
    hoursInterval: {
      type: Number,
      required: true,
    },
    hoursCurrent: {
      type: Number,
      required: true,
    },
    digits: {
      type: Number,
      required: false,
      default: 2,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    currentStateIntervalHours() {
      return processStateOfIntervalHours(
        this.hoursLatest, this.hoursInterval, this.hoursCurrent, this.digits,
      );
    },
    leftIntervalHours() {
      return processLeftIntervalHours(
        this.hoursLatest, this.hoursInterval, this.hoursCurrent, this.digits,
      );
    },
  },
};
</script>

<style scoped>

</style>
