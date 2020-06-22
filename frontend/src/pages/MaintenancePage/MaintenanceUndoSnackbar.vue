<template>
  <v-snackbar
    v-model="snackbar_state"
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
    snackbar_state: {
      type: Boolean,
      requested: true,
    }
  },
  methods: {
    undoButtonClicked() {
      this.$emit('undoButtonClicked');
    },
  }
}
</script>

<style scoped>

</style>
