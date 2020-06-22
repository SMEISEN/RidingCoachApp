<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row dense>
        <v-col cols="12" xs="12" sm="12" md="6"
               v-for="(category_object, category_name) in maintenance_object"
               v-bind:key="category_name"
        >
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">{{ category_name }}</span>
            </v-card-title>
            <MaintenanceTable
              :maintenance_entries.sync="category_object"
              @doneButtonClicked="postHistory"
            />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <MaintenanceUndoSnackbar
      :snackbar_state.sync="snackbar_state"
      @undoButtonClicked="undoMaintenance"
    />
  </v-app>
</template>

<script>
import MaintenanceTable from './MaintenanceTable';
import MaintenanceUndoSnackbar from './MaintenanceUndoSnackbar';
import {HistoryApi} from '../../components/api/HistoryApi';
import {MaintenanceApi} from '../../components/api/MaintenanceApi';

export default {
  name: 'Maintenance',
  metaInfo: {
    title: 'Maintenance',
  },
  components: {
    MaintenanceUndoSnackbar,
    MaintenanceTable,
  },
  data() {
    return {
      maintenance_object: {},
      snackbar_state: false,
      last_history_id: null,
    };
  },
  methods: {
    getMaintenance() {
      MaintenanceApi.queryMaintenance({bike_id: this.$store.getters.getCurrentBikeId})
        .then((res) => this.maintenance_object = res.data);
    },
    undoMaintenance() {
      this.snackbar_state = false;
      HistoryApi.deleteHistoryItem(this.last_history_id).then(() => this.getMaintenance());
    },
    postHistory(MtnId) {
      const payload = {
        maintenance_id: MtnId,
        bike_id: this.$store.getters.getCurrentBikeId,
        operating_hours: this.$store.getters.getCurrentBikeOperatingHours,
        comment: '',
        datetime_display: new Date().getTime(),
      };
      HistoryApi.postHistory(payload).then((res) => {
        this.getMaintenance();
        this.last_history_id = res.data;
        this.snackbar_state = true;
      });
    },
  },
  created() {
    this.getMaintenance();
    this.$store.subscribe(() => {
      this.getMaintenance();
    });
  },
  updated() {
  },
};
</script>
