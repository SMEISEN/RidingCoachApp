<template v-slot:default>
  <v-app>
    <v-flex>
      <v-layout wrap>
        <v-container>
          <v-card class="card-container">
            <v-card-title>
              <v-btn
                color="secondary"
                @click.prevent="addHistory"
              >Add maintenance entry</v-btn>
            </v-card-title>
            <HistoryTable
              :maintenance_history="orderedHistory"
              @editButtonClicked="editHistory"
            />
          </v-card>
        </v-container>
      </v-layout>
    </v-flex>
    <HistoryDialogForm
      :history_form_input.sync="history_form_object"
      :maintenance_categories="maintenance_categories_array"
      :maintenance_names="maintenance_names_object"
      @saveButtonClicked="refreshHistory"
      @cancelButtonClicked="refreshHistory"
    />
  </v-app>
</template>

<script>
import _ from 'lodash';
import HistoryTable from './HistoryTable';
import HistoryDialogForm from './HistoryDialogForm';
import {HistoryApi} from '../../components/api/HistoryApi';
import {MaintenanceApi} from '../../components/api/MaintenanceApi';


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
    },
    maintenance_categories_array: [],
    maintenance_names_object: {},
  }),
  computed: {
    orderedHistory() {
      return _.orderBy(this.history_array, 'datetime_display', 'desc');
    },
  },
  methods: {
    addHistory() {
      this.$store.commit('setHistoryEditFlag', false);
      this.$store.commit('setHistoryAddOrEditDialog', true);
    },
    editHistory(HistId) {
      HistoryApi.getHistoryItem(HistId).then((res) => {
        this.history_form_object = res.data;
        this.history_form_object.date = this.$options.filters
          .formatDateTime(res.data.datetime_display).substring(0, 10);
        this.history_form_object.time = this.$options.filters
          .formatDateTime(res.data.datetime_display).substring(11, 16);
        this.$store.commit('setHistoryEditFlag', true);
        this.$store.commit('setHistoryAddOrEditDialog', true);
      })
    },
    refreshHistory() {
      const query = {bike_id: this.$store.getters.getCurrentBikeId};
      HistoryApi.getHistory(query).then((res) => this.history_array = res.data);
      MaintenanceApi.getMaintenance().then((res) => {
        this.maintenance_categories_array = Object.keys(res.data);
        this.maintenance_names_object = res.data;
      })
    },
  },
  created() {
    this.refreshHistory();
    this.$store.subscribe(() => {
      this.refreshHistory();
    });
  },
  updated() {
  },
};
</script>
