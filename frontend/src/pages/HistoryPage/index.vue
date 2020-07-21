<template v-slot:default>
  <v-app>
    <v-flex>
      <v-layout wrap>
        <v-container>
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
      </v-layout>
    </v-flex>
    <HistoryDialogForm
      :history-form-input="history_form_object"
      :maintenance-categories="maintenance_categories_array"
      :maintenance-names="maintenance_names_object"
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
import { apiGetMaintenance } from '../../components/api/MaintenanceApi';
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
    maintenance_categories_array: [],
    maintenance_tags_array: ['checked', 'fixed', 'replaced'],
    maintenance_names_object: {},
  }),
  computed: {
    orderedHistory() {
      return this._.orderBy(this.history_array, 'datetime_display', 'desc');
    },
  },
  created() {
    this.refreshHistory();
  },
  updated() {
  },
  methods: {
    addHistory() {
      this.history_form_object.operating_hours = this.$store.getters.getCurrentBikeOperatingHours;
      this.$store.commit('setHistoryEditFlag', false);
      this.$store.commit('setHistoryAddOrEditDialog', true);
    },
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
      apiGetMaintenance()
        .then((res) => {
          this.maintenance_categories_array = Object.keys(res.data);
          this.maintenance_names_object = res.data;
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
