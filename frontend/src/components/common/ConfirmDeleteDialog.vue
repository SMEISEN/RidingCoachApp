<template>
  <v-dialog
    v-model="confirm_delete_dialog"
    persistent max-width="400"
  >
    <v-card>
      <v-card-title class="headline">
        Warning
      </v-card-title>
      <v-card-text>
        <p class="text--primary">
          Do you really want to delete this {{ flagged_for_deletion }}?</p>
        <p class="text--secondary text-sm-left">
          The deletion is permanent and cannot be undone.</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="accent"
          text
          @click.prevent="onCancel"
        >Cancel</v-btn>
        <v-btn
          color="error"
          text
          @click.prevent="onConfirm"
        >Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDeleteDialog',
  props: {
    flagged_for_deletion: {
      type: String,
      required: true,
    },
  },
  computed: {
    confirm_delete_dialog: {
      get() {
        return this.$store.getters.getHistoryDeleteDialog;
      },
      set(value) {
        this.$store.commit('setHistoryDeleteDialog', value);
      }
    },
  },
  methods: {
    onCancel() {
      this.$store.commit('setHistoryDeleteDialog', false);
    },
    onConfirm() {
      this.$emit('deleteConfirmationButtonClicked');
      this.$store.commit('setHistoryDeleteDialog', false);
    },
  },
}
</script>

<style scoped>

</style>
