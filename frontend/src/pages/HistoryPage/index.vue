<template>
  <v-app>
    <v-container fluid>
      <v-card class="card-container">
        <v-card-title>
          <v-btn
            color="secondary"
            @click.prevent="addHistory()"
          >
            Add maintenance entry
          </v-btn>
        </v-card-title>
        <HistoryTable
          :maintenance-history="orderedHistory"
          @editButtonClicked="editHistory"
          @deletionConfirmed="refreshHistory()"
        />
      </v-card>
    </v-container>
    <HistoryDialogForm
      :history-form-input="history_form_object"
      :maintenance-categories="maintenance_categories_array"
      :maintenance-array="maintenance_array"
      :maintenance-tags="maintenance_tags_array"
      @saveButtonClicked="refreshHistory()"
      @cancelButtonClicked="refreshHistory()"
    />
  </v-app>
</template>

<script>
import {
  apiGetHistoryItem,
  apiQueryHistory,
} from '../../components/api/HistoryApi';
import { apiQueryMaintenance } from '../../components/api/MaintenanceApi';
import HistoryTable from './HistoryTable.vue';
import HistoryDialogForm from './HistoryDialogForm.vue';

export default {
  name: 'History',
  metaInfo: {
    title: 'History',
  },
  components: {
    HistoryTable,
    HistoryDialogForm,
  },
  data: () => ({
    history_array: [],
    history_form_object: {
      history_id: null,
      maintenance_id: null,
      category: null,
      name: null,
      operating_hours: null,
      date: new Date().toISOString().substr(0, 10),
      time: new Date().toTimeString().substr(0, 5),
      comment: null,
      tags: null,
    },
    maintenance_array: [],
    maintenance_categories_array: [],
    maintenance_tags_array: ['checked', 'fixed', 'replaced'],
  }),
  computed: {
    orderedHistory() {
      return this._.orderBy(this.history_array, 'datetime_display', 'desc');
    },
    currentBikeId() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  created() {
    this.refreshHistory();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'selectBike') {
        this.refreshHistory();
      }
    });
  },
  methods: {
    /**
     * Gets current operating hours of the selected bike and opens the add history dialog.
     */
    addHistory() {
      this.history_form_object.operating_hours = this.$store.getters.getCurrentBikeOperatingHours;
      this.$store.commit('setHistoryEditFlag', false);
      this.$store.commit('setHistoryAddOrEditDialog', true);
    },
    /**
     * Opens the edit history dialog for a specific history entry.
     * @param {String} HistId history uuid4 string
     */
    editHistory(HistId) {
      apiGetHistoryItem(HistId)
        .then((res) => {
          this.history_form_object = res.data;
          this.history_form_object.date = this.$options.filters
            .formatDateTime(res.data.datetime_display).substring(0, 10);
          this.history_form_object.time = this.$options.filters
            .formatDateTime(res.data.datetime_display).substring(11, 16);
          this.$store.commit('setHistoryEditFlag', true);
          this.$store.commit('setHistoryAddOrEditDialog', true);
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
     * Reload the history entries of the selected bike.
     */
    refreshHistory() {
      const query = { bike_id: this.$store.getters.getCurrentBikeId };
      apiQueryHistory(query)
        .then((res) => {
          this.history_array = res.data;
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
      apiQueryMaintenance({ bike_id: this.currentBikeId })
        .then((res) => {
          this.maintenance_array = res.data;
          this.maintenance_categories_array = this._.uniq(res.data.map((value) => value.category));
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
