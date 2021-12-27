<template>
  <div>
    <v-simple-table
      fixed-header
    >
      <thead>
        <tr>
          <th class="text-left">
            Category
          </th>
          <th
            class="text-left"
            style="min-width: 120px"
          >
            Name
          </th>
          <th class="text-left">
            Hours
          </th>
          <th class="text-left">
            Date
          </th>
          <th
            class="button"
            style="min-width: 140px"
          >
            Tags
          </th>
          <th class="text-left">
            Comment
          </th>
          <th class="button" />
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(maintenance) in maintenanceHistory"
          :key="maintenance.history_id"
        >
          <td style="font-size: 12px">
            {{ maintenance.category }}
          </td>
          <td style="font-size: 12px">
            {{ maintenance.name }}
          </td>
          <td>
            {{ maintenance.operating_hours }}
          </td>
          <td>
            {{ maintenance.datetime_display | formatDateTime }}
          </td>
          <td>
            <div
              v-if="maintenance.tags !== null"
              class="btn-group"
              role="group"
            >
              <v-tooltip
                v-if="maintenance.tags.includes('checked')"
                bottom
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-avatar
                    size="32"
                    v-bind="attrs"
                    v-on="on"
                  >
                    <v-icon color="success">
                      mdi-check-circle-outline
                    </v-icon>
                  </v-avatar>
                </template>
                <span>{{ 'checked' }}</span>
              </v-tooltip>
              <v-tooltip
                v-if="maintenance.tags.includes('fixed')"
                bottom
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-avatar
                    size="32"
                    v-bind="attrs"
                    v-on="on"
                  >
                    <v-icon color="warning">
                      mdi-progress-wrench
                    </v-icon>
                  </v-avatar>
                </template>
                <span>{{ 'fixed' }}</span>
              </v-tooltip>
              <v-tooltip
                v-if="maintenance.tags.includes('replaced')"
                bottom
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-avatar
                    size="32"
                    v-bind="attrs"
                    v-on="on"
                  >
                    <v-icon color="error">
                      mdi-refresh
                    </v-icon>
                  </v-avatar>
                </template>
                <span>{{ 'replaced' }}</span>
              </v-tooltip>
            </div>
          </td>
          <td>
            {{ maintenance.comment }}
          </td>
          <td>
            <div
              class="btn-group"
              role="group"
            >
              <v-btn
                color="warning"
                text
                @click.prevent="onEditButton(maintenance.history_id)"
              >
                Edit
              </v-btn>
              <v-btn
                color="error"
                text
                @click.prevent="onDeleteButton(maintenance.history_id)"
              >
                Delete
              </v-btn>
            </div>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'history entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import { apiDeleteHistoryItem } from '../../components/api/HistoryApi';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';

export default {
  name: 'HistoryTable',
  components: {
    ConfirmDeleteDialog,
  },
  props: {
    maintenanceHistory: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    history_id: null,
    confirm_delete_dialog: false,
  }),
  methods: {
    /**
     * Emits message to parent that the edit button of a specific history entry was clicked.
     * @param {String} HistId history uuid4 string
     */
    onEditButton(HistId) {
      this.history_id = HistId;
      this.$emit('editButtonClicked', this.history_id);
    },
    /**
     * Emits message to parent that the delete button of a specific history entry was clicked.
     * @param {String} HistId history uuid4 string
     */
    onDeleteButton(HistId) {
      this.history_id = HistId;
      this.confirm_delete_dialog = true;
    },
    /**
     * Emits message to parent that the confirm deletion dialog was confirmed.
     */
    deletionConfirmed() {
      apiDeleteHistoryItem(this.history_id)
        .then(() => {
          this.$emit('deletionConfirmed', this.history_id);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: 'Maintenance history entry deleted!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>
