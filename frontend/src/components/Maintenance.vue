<template>
  <v-app>
    <v-flex>
      <v-layout wrap>
        <v-container v-for="(category, key) in maintenance_dict" v-bind:key="key">
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">{{ key }}</span>
            </v-card-title>
            <v-row>
              <v-col sm="10">
                <v-simple-table height="300px">
                  <thead>
                  <tr>
                    <th class="text-left">Name</th>
                    <th class="text-left">Hours left</th>
                    <th class="text-left">State</th>
                    <th></th>
                    <th class="text-left">Interval</th>
                    <th class="text-left">Date</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(maintenance) in category" v-bind:key="maintenance.mtn_id">
                    <td>{{ maintenance.name }}</td>
                    <td v-if="maintenance.hours_last == null"></td>
                    <td v-else>
                      {{
                      bike_operating_hours -
                      maintenance.hours_last +
                      maintenance.hours_interval
                      }} h
                    </td>
                    <td v-if="maintenance.hours_last == null"></td>
                    <td v-else>
                      <v-progress-linear
                        color="primary"
                        background-color="secondary"
                        height="10"
                        value="
                        (bike_operating_hours -
                        maintenance.hours_last +
                        maintenance.hours_interval)
                        / maintenance.hours_interval"
                        rounded>
                      </v-progress-linear>
                    </td>
                    <td>
                      <v-btn color="success" text @click="editMaintenance(maintenance.mtn_id)">
                        Done!
                      </v-btn>
                    </td>
                    <td>{{ maintenance.hours_interval }} h</td>
                    <td v-if="maintenance.hours_last == null"></td>
                    <td v-else>
                      {{ maintenance.datetime_last_modified | formatDateTime }}
                    </td>
                  </tr>
                  </tbody>
                </v-simple-table>
              </v-col>
            </v-row>
          </v-card>
          <br>
        </v-container>
      </v-layout>
    </v-flex>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Maintenance',
  data() {
    return {
      maintenance_dict: {
        Motor: [],
        Carburetor: [],
        Attachments: [],
        Brakes: [],
        Clutch: [],
        Suspension: [],
        Wheels: [],
      },
      bike_operating_hours: '',
      history_entry_dict: {
        hist_id: '',
        category: '',
        name: '',
        hours: '',
        date: '',
        time: '',
        comment: '',
      },
      maintenance_entry: {
        mtn_id: '',
        category: '',
        name: '',
        hours_interval: '',
        hours_last: '',
        datetime_created: '',
        datetime_last_modified: '',
      },
    };
  },
  methods: {
    getMaintenance() {
      const ApiPath = '/api/maintenance';
      axios.get(ApiPath)
        .then((res) => {
          this.maintenance_dict.Motor = res.data.Motor;
          this.maintenance_dict.Carburetor = res.data.Carburetor;
          this.maintenance_dict.Attachments = res.data.Attachments;
          this.maintenance_dict.Brakes = res.data.Brakes;
          this.maintenance_dict.Clutch = res.data.Clutch;
          this.maintenance_dict.Suspension = res.data.Suspension;
          this.maintenance_dict.Wheels = res.data.Wheels;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBikeEngineHours() {
      const ApiPath = 'api/bike';
      axios.get(ApiPath)
        .then((res) => {
          this.bike_operating_hours = res.data.operating_hours;
        });
    },
    getMaintenanceEntry(MtnId) {
      const ApiPath = `/api/maintenance/${MtnId}`;
      return axios.get(ApiPath)
        .then(() => axios.get(ApiPath))
        .catch((error) => {
          console.log(error);
          this.getMaintenance();
        });
    },
    async editMaintenance(MtnId) {
      await this.getMaintenanceEntry(MtnId)
        .then((res) => {
          this.postHistory({
            category: res.data.category,
            name: res.data.name,
            hours: this.bike_operating_hours,
            datetime_display: new Date().getTime(),
            comment: '',
          });
        });
      this.putMaintenance(MtnId, { hours_last: this.bike_operating_hours });
    },
    putMaintenance(MtnId, payload) {
      const ApiPath = `/api/maintenance/${MtnId}`;
      axios.put(ApiPath, payload)
        .then(() => {
          this.getMaintenance();
        })
        .catch((error) => {
          console.log(error);
          this.getMaintenance();
        });
    },
    postHistory(payload) {
      const ApiPath = '/api/history';
      axios.post(ApiPath, payload)
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getBikeEngineHours();
    this.getMaintenance();
  },
};
</script>
