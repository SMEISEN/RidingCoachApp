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
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Attachments
        </v-btn>
        <v-btn
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Brakes
        </v-btn>
        <v-btn
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Carburetor
        </v-btn>
        <v-btn
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Engine
        </v-btn>
        <v-btn
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Suspension
        </v-btn>
        <v-btn
          color="white"
          class="primary--text ma-1"
          style="min-width:16%"
          x-small
        >
          Wheels
        </v-btn>
      </v-row>
    </v-btn-toggle>
  </v-toolbar>
</template>

<script>
export default {
  name: 'SparepartsToolbar',
  props: {
    sparepartsButtons: {
      type: Number,
      required: true,
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
