<template>
  <v-dialog
    v-model="confirmDeleteDialog"
    persistent
    max-width="400"
  >
    <v-card>
      <v-card-title class="headline">
        Warning
      </v-card-title>
      <v-card-text>
        <p class="text--primary">
          Do you really want to delete this {{ flaggedForDeletion }}?
        </p>
        <p class="text--secondary text-sm-left">
          The deletion is permanent and cannot be undone.
        </p>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="accent"
          text
          @click.prevent="onCancel"
        >
          Cancel
        </v-btn>
        <v-btn
          color="error"
          text
          @click.prevent="onConfirm"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDeleteDialog',
  props: {
    confirmDeleteDialog: {
      type: Boolean,
      required: true,
    },
    flaggedForDeletion: {
      type: String,
      required: true,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    onCancel() {
      this.$emit('cancelButtonClicked');
      this.$emit('update:confirm_delete_dialog', false);
    },
    onConfirm() {
      this.$emit('deleteConfirmationButtonClicked');
      this.$emit('update:confirm_delete_dialog', false);
    },
  },
};
</script>

<style scoped>

</style>
