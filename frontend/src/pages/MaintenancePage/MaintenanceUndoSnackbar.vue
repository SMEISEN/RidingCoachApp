<template>
  <v-snackbar
    v-model="snackbar_state"
    :timeout="3000"
    color="info"
  >
    Maintenance history added!
    <v-btn
      text
      @click="undoButtonClicked()"
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
  computed: {
    snackbar_state: {
      get() {
        return this.snackbarState;
      },
      set(value) {
        this.$emit('update:snackbarState', value);
      },
    },
  },
  methods: {
    /**
     * Emits a message to the parent component that the undo button of the snackbar was clicked and
     * closes the snackbar dialog.
     */
    undoButtonClicked() {
      this.$emit('undoButtonClicked');
      this.$emit('update:snackbarState', false);
    },
  },
};
</script>
