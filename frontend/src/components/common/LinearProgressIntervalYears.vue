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
      const latest = new Date(this.date_latest);
      const now = new Date();
      const start = new Date(latest.getFullYear(), 0, 0);
      const diff = now - start;
      const oneDay = 1000 * 60 * 60 * 24;
      const day = Math.floor(diff / oneDay);
      const days_left = 365 - day;

      return Number.parseFloat(days_left.toPrecision(this.digits));
    },
    currentStateIntervalYears() {
      const latest = new Date(this.date_latest);
      const now = new Date();
      const start = new Date(latest.getFullYear(), 0, 0);
      const diff = now - start;
      const oneDay = 1000 * 60 * 60 * 24;
      const day = Math.floor(diff / oneDay);
      const state = (day / 365) * 100;

      return Number.parseFloat(state.toPrecision(this.digits));
    },
  }
}
</script>

<style scoped>

</style>
