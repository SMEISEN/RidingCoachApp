<template>
  <v-progress-linear
    color="primary"
    background-color="accent"
    height="22"
    :value="currentStateIntervalYears()"
    rounded
  >
    <template v-slot="{ value }">
      <span class="white--text">
        {{ leftIntervalYears() }} d /
        {{ Math.ceil(value) }} %
      </span>
    </template>
  </v-progress-linear>
</template>

<script>
import {
  processLeftIntervalYears,
  processStateOfIntervalYears,
} from '../utils/DataProcessingUtils';

export default {
  name: 'LinearProgressIntervalYears',
  props: {
    dateLatest: {
      type: String,
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
    leftIntervalYears() {
      return processLeftIntervalYears(this.dateLatest, this.digits);
    },
    currentStateIntervalYears() {
      return processStateOfIntervalYears(this.dateLatest, this.digits);
    },
  },
};
</script>

<style scoped>

</style>
