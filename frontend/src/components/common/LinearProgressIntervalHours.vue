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
      const state = ((this.hours_latest + this.hours_interval - this.hours_current)
        / this.hours_interval) * 100;
      return Number.parseFloat(state.toPrecision(this.digits));
    },
    leftIntervalHours() {
      const hours_left = this.hours_latest + this.hours_interval - this.hours_current;
      return Number.parseFloat(hours_left.toPrecision(this.digits));
    },
  },
}
</script>

<style scoped>

</style>
