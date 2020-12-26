<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row dense>
        <v-col
          v-for="(category_object, category_name) in maintenance_object"
          :key="category_name + '/' + Object.keys(category_object).length"
          cols="12"
          xs="12"
          sm="12"
          md="6"
        >
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">{{ category_name }}</span>
            </v-card-title>
            <MaintenanceTable
              :maintenance-entries="category_object"
              @doneButtonClicked="postHistoryEntry"
            />
            <MaintenanceDial
              :category-object="category_object"
              :category-name="category_name"
              :category-array="category_array"
              @refreshTable="getMaintenance"
            />
          </v-card>
        </v-col>
        <MaintenanceAddCategoryDialog />
      </v-row>
    </v-container>
    <MaintenanceUndoSnackbar
      :snackbar-state.sync="snackbar_state"
      @undoButtonClicked="undoMaintenance"
    />
  </v-app>
</template>

<script>
import {
  apiDeleteHistoryItem,
  apiPostHistory,
} from '../../components/api/HistoryApi';
import { apiQueryMaintenance } from '../../components/api/MaintenanceApi';
import MaintenanceTable from './MaintenanceTable.vue';
import MaintenanceUndoSnackbar from './MaintenanceUndoSnackbar.vue';
import MaintenanceDial from './MaintenanceDial.vue';
import MaintenanceAddCategoryDialog from './MaintenanceAddCategoryDialog.vue';

export default {
  name: 'Maintenance',
  metaInfo: {
    title: 'Maintenance',
  },
  components: {
    MaintenanceDial,
    MaintenanceUndoSnackbar,
    MaintenanceTable,
    MaintenanceAddCategoryDialog,
  },
  data() {
    return {
      maintenance_object: {},
      interval_types: [],
      snackbar_state: false,
    };
  },
  computed: {
    currentBikeId() {
      return this.$store.getters.getCurrentBikeId;
    },
    currentBikeHours() {
      return this.$store.getters.getCurrentBikeOperatingHours;
    },
    lastHistoryId: {
      get() {
        return this.$store.getters.getHistoryId();
      },
      set(value) {
        this.$store.commit('setHistoryId', value);
      },
    },
    category_array() {
      return Object.keys(this.maintenance_object);
    },
  },
  created() {
    this.getMaintenance();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'selectBike') {
        this.getMaintenance();
      }
    });
  },
  updated() {
  },
  methods: {
    getMaintenance() {
      apiQueryMaintenance({ bike_id: this.currentBikeId })
        .then((res) => {
          this.maintenance_object = res.data;
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    undoMaintenance() {
      apiDeleteHistoryItem(this.lastHistoryId)
        .then(() => {
          this.getMaintenance();
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
    postHistoryEntry(mtnId, selectedChips) {
      const payload = {
        maintenance_id: mtnId,
        bike_id: this.currentBikeId,
        operating_hours: this.currentBikeHours,
        comment: '',
        tags: selectedChips,
        datetime_display: new Date().getTime() / 1000,
      };
      apiPostHistory(payload)
        .then((res) => {
          this.getMaintenance();
          this.lastHistoryId = res.data;
          this.snackbar_state = true;
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Maintenance history entry added!',
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
