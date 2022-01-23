<template>
  <div>
    <v-dialog
      v-model="deleteMaintenanceDialog"
      persistent
    >
      <v-form
        ref="validation_form"
        v-model="valid"
      >
        <v-card>
          <v-card-title>
            <span class="headline">Delete maintenance interval: {{ categoryName }}</span>
          </v-card-title>
          <v-card-text>
            <MaintenanceDialDeleteDialogTable
              :category-array="categoryArray"
              :delete-checkbox="delete_checkbox"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="secondary"
              text
              @click.prevent="onCancel"
            >
              Close
            </v-btn>
            <v-btn
              color="secondary"
              :disabled="!valid"
              text
              @click.prevent="onDelete"
            >
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'maintenance work selection'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import MaintenanceDialDeleteDialogTable from './MaintenanceDialDeleteDialogTable.vue';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';
import { apiDeleteMaintenanceItem } from '../../components/api/MaintenanceApi';

export default {
  name: 'MaintenanceDialDeleteDialog',
  components: {
    ConfirmDeleteDialog,
    MaintenanceDialDeleteDialogTable,
  },
  props: {
    deleteMaintenanceDialog: {
      type: Boolean,
      required: true,
    },
    categoryArray: {
      type: Array,
      required: true,
    },
    categoryName: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    valid: true,
    delete_checkbox: {},
    confirm_delete_dialog: false,
  }),
  methods: {
    /**
     * Emits a message to the parent component that the maintenance deletion was canceled.
     */
    onCancel() {
      this.$emit('update:deleteMaintenanceDialog', false);
    },
    /**
     * Closes the confirm deletion dialog.
     */
    onDelete() {
      this.confirm_delete_dialog = true;
    },
    /**
     * Confirms the deletion of a maintenance item.
     */
    deletionConfirmed() {
      const entries = Object.entries(this.delete_checkbox);
      for (let i = 0; i < entries.length; i += 1) {
        const name = entries[i][0];
        const deleteFlag = entries[i][1];
        const mtnId = this.categoryArray.filter((j) => j.name === name)[0].maintenance_id;
        const index = this.categoryArray.indexOf(this.categoryArray.filter(
          (j) => j.name === this.maintenance_name,
        )[0]);
        if (deleteFlag === true) {
          apiDeleteMaintenanceItem(mtnId)
            .then(() => {
              delete this.categoryArray[index];
              this.$emit('maintenanceDeleted');
            })
            .catch((error) => {
              this.$store.commit('setInfoSnackbar', {
                state: true,
                color: 'error',
                message: `${error}!`,
              });
            });
        }
      }
      this.$emit('update:deleteMaintenanceDialog', false);
    },
  },
};
</script>
