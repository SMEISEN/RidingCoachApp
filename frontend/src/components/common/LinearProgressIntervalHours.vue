<template>
  <v-progress-linear
    color="primary"
    background-color="accent"
    height="22"
    :value="currentStateIntervalHours()"
    rounded>
    <template v-slot="{ value }">
                      <span class="white--text">
                        {{ leftIntervalHours() }} h /
                        {{ Math.ceil(value) }} %
                      </span>
    </template>
  </v-progress-linear>
</template>

<script>
import {DataProcessingUtils} from './DataProcessingUtils';

export default {
  name: 'LinearProgressIntervalHours',
  props: {
    hours_latest: {
      type: Number,
      required: true,
    },
    hours_interval: {
      type: Number,
      required: true,
    },
    hours_current: {
      type: Number,
      required: true,
    },
    digits: {
      type: Number,
      required: false,
      default: 2,
    }
  },
  methods: {
    currentStateIntervalHours() {
      return DataProcessingUtils
        .processStateOfIntervalHours(this.hours_latest, this.hours_interval, this.hours_current)
    },
    leftIntervalHours() {
      return DataProcessingUtils
        .processLeftIntervalHours(this.hours_latest, this.hours_interval, this.hours_current)
    },
  },
}
</script>

<style scoped>

</style>
