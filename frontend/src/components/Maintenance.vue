<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row dense>
        <v-col cols="12" xs="12" sm="12" md="6"
               v-for="(category_object, category_name) in maintenance_dict"
               v-bind:key="category_name"
        >
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">{{ category_name }}</span>
            </v-card-title>
            <v-simple-table dense fixed-header height="300px">
              <thead>
              <tr>
                <th class="text-left" style="min-width: 120px">
                  Name
                </th>
                <th class="text-left" style="min-width: 120px;width: 120px;max-width: 120px">
                  State
                </th>
                <th class="button" style="min-width: 120px;width: 120px;max-width: 120px"></th>
                <th class="text-left" style="min-width: 80px;width: 80px;max-width: 80px">
                  Interval
                </th>
                <th class="text-left" style="width: 145px">
                  Date
                </th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="maintenance_object in sort_maintenance(category_object)"
                  v-bind:key="maintenance_object.maintenance_id">
                <td style="font-size: 12px">{{ maintenance_object.name }}</td>
                <td v-if="!Object.keys(maintenance_object).includes('operating_hours')"></td>
                <td v-else-if="maintenance_object.interval_unit === 'a'">
                  <v-progress-linear
                    color="primary"
                    background-color="accent"
                    height="22"
                    :value="currentStateIntervalYears(maintenance_object.datetime_display)"
                    rounded>
                    <template v-slot="{ value }">
                      <span class="white--text">
                        {{ leftIntervalYears(maintenance_object.datetime_display) }} a /
                        {{ Math.ceil(value) }} %
                      </span>
                    </template>
                  </v-progress-linear>
                </td>
                <td v-else>
                  <v-progress-linear
                    color="primary"
                    background-color="accent"
                    height="22"
                    :value="currentStateIntervalHours(maintenance_object.operating_hours,
                                                      maintenance_object.interval_amount,
                                                      $store.getters.getCurrentBikeOperatingHours)"
                    rounded>
                    <template v-slot="{ value }">
                      <span class="white--text">
                        {{ leftIntervalHours(maintenance_object.operating_hours,
                                             maintenance_object.interval_amount,
                                             $store.getters.getCurrentBikeOperatingHours) }} h /
                        {{ Math.ceil(value) }} %
                      </span>
                    </template>
                    </v-progress-linear>
                </td>
                <td>
                  <v-btn color="success" text
                         @click="editMaintenance(maintenance_object.maintenance_id)">
                    Done!
                  </v-btn>
                </td>
                <td>
                  {{ maintenance_object.interval_amount }} {{ maintenance_object.interval_unit }}
                </td>
                <td v-if="!Object.keys(maintenance_object).includes('operating_hours')"> </td>
                <td v-else>
                  {{ maintenance_object.datetime_display | formatDateTime }}
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar
      v-model="snackbar"
      :timeout="3000"
      color="info"
    >
      Maintenance history added!
      <v-btn
        text
        @click="undoMaintenance"
      >
        Undo
      </v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

export default {
  name: 'Maintenance',
  metaInfo: {
    title: 'Maintenance',
  },
  data() {
    return {
      maintenance_dict: {},
      snackbar: false,
      last_history_id: null,
    };
  },
  methods: {
    sort_maintenance(maintenanceObject) {
      const maintenanceList = [];
      for (let i = 0; i < Object.keys(maintenanceObject).length; i += 1) {
        maintenanceList.push(
          Object.assign(Object.values(maintenanceObject)[i],
            { name: Object.keys(maintenanceObject)[i] }),
        );
      }
      return _.orderBy(maintenanceList,
        ['interval_unit', 'interval_amount'], ['desc', 'asc']);
    },
    currentStateIntervalHours(Latest, Interval, Current) {
      const state = ((Latest + Interval - Current) / Interval) * 100;
      return Number.parseFloat(state.toPrecision(2));
    },
    leftIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      const HoursLeft = HoursLatest + HoursInterval - BikeHours;
      return Number.parseFloat(HoursLeft.toPrecision(2));
    },
    currentStateIntervalYears(Latest) {
      const latest = new Date(Latest);
      const now = new Date();
      const start = new Date(latest.getFullYear(), 0, 0);
      const diff = now - start;
      const oneDay = 1000 * 60 * 60 * 24;
      const day = Math.floor(diff / oneDay);

      return (day / 365) * 100;
    },
    leftIntervalYears(Latest) {
      const latest = new Date(Latest);
      const now = new Date();
      const start = new Date(latest.getFullYear(), 0, 0);
      const diff = now - start;
      const oneDay = 1000 * 60 * 60 * 24;
      const day = Math.floor(diff / oneDay);

      return 365 - day;
    },
    getMaintenance() {
      const ApiPath = '/api/maintenance/query';
      const payload = {
        bike_id: this.$store.getters.getCurrentBikeId,
      };
      axios.post(ApiPath, payload)
        .then((res) => {
          this.maintenance_dict = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    editMaintenance(MtnId) {
      this.postHistory({
        maintenance_id: MtnId,
        bike_id: this.$store.getters.getCurrentBikeId,
        operating_hours: this.$store.getters.getCurrentBikeOperatingHours,
        comment: '',
        datetime_display: new Date().getTime(),
      });
    },
    undoMaintenance() {
      this.deleteHistory();
      this.snackbar = false;
    },
    postHistory(payload) {
      const ApiPath = '/api/history';
      axios.post(ApiPath, payload)
        .then((res) => {
          this.getMaintenance();
          this.last_history_id = res.data;
          this.snackbar = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteHistory() {
      const ApiPath = `/api/history/${this.last_history_id}`;
      axios.delete(ApiPath)
        .then(() => {
          this.getMaintenance();
        })
        .catch((error) => {
          console.error(error);
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
