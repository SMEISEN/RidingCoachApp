<template>
  <v-app>
    <v-container fluid>
      <v-row dense>
        <v-col
          v-for="(category_array, category_name) in maintenance_object"
          :key="category_name + '/' + category_array.length"
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
              :maintenance-entries="category_array"
              @doneButtonClicked="postHistoryEntry"
            />
            <MaintenanceDial
              :category-array="category_array"
              :category-name="category_name"
              :category-names="category_names"
              @refreshTable="getMaintenance"
            />
          </v-card>
        </v-col>
        <MaintenanceAddCategoryDialog
          :category-names="category_names"
          @refreshTable="getMaintenance"
        />
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
      category_names: [],
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
        return this.$store.getters.getHistoryId;
      },
      set(value) {
        this.$store.commit('setHistoryId', value);
      },
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
  methods: {
    /**
     * Gets the maintenance items for the selected bike.
     */
    getMaintenance() {
      apiQueryMaintenance({ bike_id: this.currentBikeId })
        .then((res) => {
          this.maintenance_object = this.structureMaintenanceArray(res.data);
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    /**
     * Deletes the most recent maintenance history entry.
     */
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
    /**
     * Adds a new maintenance history entry.
     * @param {string} mtnId maintenance id
     * @param {array} selectedChips array of strings with the selected maintenance tags
     */
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
    structureMaintenanceArray(maintenanceArray) {
      this.category_names = this._.uniq(maintenanceArray.map((value) => value.category));
      const maintenanceObject = {};
      for (let i = 0; i < this.category_names.length; i += 1) {
        const categoryName = this.category_names[i];
        const categoryObject = {};
        categoryObject[categoryName] = maintenanceArray.filter(
          (j) => j.category === categoryName,
        );
        Object.assign(maintenanceObject, categoryObject);
      }
      return maintenanceObject;
    },
  },
};
</script>
