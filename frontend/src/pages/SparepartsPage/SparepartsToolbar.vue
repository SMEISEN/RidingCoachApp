<template>
  <v-toolbar
    top
    short
    flat
  >
    <v-btn-toggle
      v-model="spareparts_buttons"
      dense
      style="width:100%"
      class="primary--text"
      active-class="v-btn--active-toolbar"
    >
      <v-row justify="center">
        <v-btn
          v-for="(module, i) in bikeModules"
          :key="i"
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          {{ module }}
        </v-btn>
      </v-row>
    </v-btn-toggle>
  </v-toolbar>
</template>

<script>
export default {
  name: 'SparepartsToolbar',
  props: {
    bikeModules: {
      type: Array,
      required: true,
    },
    sparepartsButtons: {
      type: [Number, null],
      required: false,
      default: null,
    },
  },
  computed: {
    spareparts_buttons: {
      get() {
        return this.sparepartsButtons;
      },
      set(value) {
        this.$emit('update:sparepartsButtons', value);
      },
    },
  },
};
</script>

<style scoped>

</style>
