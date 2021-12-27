<template>
  <v-snackbar
    v-model="snackbar_state"
    top
    right
    text
    outlined
    :color="snackbar_color"
    :timeout="3000"
  >
    {{ snackbar_message }}
  </v-snackbar>
</template>

<script>
export default {
  name: 'TheInfoSnackbar',
  computed: {
    snackbar_state: {
      get() {
        return this.$store.getters.getInfoSnackbarState;
      },
      set(value) {
        this.$store.commit('setInfoSnackbarState', value);
      },
    },
    snackbar_color() {
      return this.$store.getters.getInfoSnackbarColor;
    },
    snackbar_message() {
      return this.$store.getters.getInfoSnackbarMessage;
    },
  },
};
</script>
