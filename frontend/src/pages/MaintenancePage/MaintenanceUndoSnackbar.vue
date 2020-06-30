<template>
  <v-snackbar
    v-model="snackbarState"
    :timeout="3000"
    color="info"
  >
    Maintenance history added!
    <v-btn
      text
      @click="undoButtonClicked"
    >
      Undo
    </v-btn>
  </v-snackbar>
</template>

<script>
export default {
  name: 'MaintenanceUndoSnackbar',
  props: {
    snackbarState: {
      type: Boolean,
      requested: true,
    },
  },
  created() {
  },
  updated() {
  },
  methods: {
    undoButtonClicked() {
      this.$emit('undoButtonClicked');
    },
  },
};
</script>

<style scoped>

</style>
