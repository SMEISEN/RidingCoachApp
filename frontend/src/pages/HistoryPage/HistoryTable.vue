<template>
  <div>
    <v-simple-table fixed-header height="500px">
      <thead>
      <tr>
        <th class="text-left">Category</th>
        <th class="text-left" style="min-width: 120px">Name</th>
        <th class="text-left">Hours</th>
        <th class="text-left">Date</th>
        <th class="text-left">Comment</th>
        <th></th>
      </tr>
      </thead>
      <tbody>
      <tr
        v-for="(maintenance) in maintenance_history"
        v-bind:key="maintenance.history_id"
        v-bind:MtnId="maintenance.history_id"
      >
        <td style="font-size: 12px">{{ maintenance.category }}</td>
        <td style="font-size: 12px">{{ maintenance.name }}</td>
        <td>{{ maintenance.operating_hours }}</td>
        <td>{{ maintenance.datetime_display | formatDateTime }}</td>
        <td>{{ maintenance.comment }}</td>
        <td>
          <div class="btn-group" role="group">
            <v-btn
              color="warning"
              text
              @click.prevent="onEditButton(maintenance.history_id)"
            >Edit</v-btn>
            <v-btn
              color="error"
              text
              @click="onDeleteButton(maintenance.history_id)"
            >Delete</v-btn>
          </div>
        </td>
      </tr>
      </tbody>
    </v-simple-table>
    <ConfirmDeleteDialog
      :flagged_for_deletion="'history entry'"
      @deleteConfirmationButtonClicked="deletionConfirmed"
    />
  </div>
</template>


<script>
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog';
import {HistoryApi} from '../../components/common/HistoryApi';

export default {
  name: 'HistoryTable',
  components: {
    ConfirmDeleteDialog,
  },
  props: {
    maintenance_history: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    history_id: null,
  }),
  methods: {
    onEditButton(HistId) {
      this.history_id = HistId;
      this.$emit('editButtonClicked', this.history_id);
    },
    onDeleteButton(HistId) {
      this.history_id = HistId;
      this.$store.commit('setHistoryDeleteDialog', true);
    },
    deletionConfirmed() {
      HistoryApi.deleteHistoryItem(this.history_id);
    }
  },
  created() {
  },
  updated() {
  },
}
</script>

<style scoped>

</style>
