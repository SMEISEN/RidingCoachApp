<template>
  <v-progress-linear
    color="primary"
    background-color="accent"
    height="22"
    :value="currentStateIntervalYears()"
    rounded>
    <template v-slot="{ value }">
                      <span class="white--text">
                        {{ leftIntervalYears() }} d /
                        {{ Math.ceil(value) }} %
                      </span>
    </template>
  </v-progress-linear>
</template>

<script>
import {DataProcessingUtils} from "./DataProcessingUtils";

export default {
  name: 'LinearProgressIntervalYears',
  props: {
    date_latest: {
      type: String,
      required: true,
    },
    digits: {
      type: Number,
      required: false,
      default: 2,
    }
  },
  methods: {
    leftIntervalYears() {
      return DataProcessingUtils.processLeftIntervalYears(this.date_latest, this.digits);
    },
    currentStateIntervalYears() {
      return DataProcessingUtils.processStateOfIntervalYears(this.date_latest, this.digits);
    },
  }
}
</script>

<style scoped>

</style>
