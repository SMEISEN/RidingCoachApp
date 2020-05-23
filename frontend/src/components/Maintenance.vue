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
                    <td>{{ maintenance.hours_left }}</td>
                    <td>{{ maintenance.state }}</td>
                    <td>
                      <v-btn color="success" text @click="putMaintenance(maintenance.mtn_id)">
                        Done!
                      </v-btn>
                    </td>
                    <td>{{ maintenance.hours_interval }}</td>
                    <td>{{ maintenance.datetime_display | formatDateTime }}</td>
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
      bike_dict: {
        operating_hours: '',
        manufacturer: '',
        model: '',
        ccm: '',
        stroke: '',
        piston: '',
        year: '',
      },
    };
  },
  methods: {
    getMaintenance() {
      const path = '/api/maintenance';
      axios.get(path)
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
      const path = 'api/bike';
      axios.get(path)
        .then((res) => {
          this.bike.operating_hours = res.data.operating_hours;
          this.bike.manufacturer = res.data.manufacturer;
          this.bike.model = res.data.model;
          this.bike.ccm = res.data.ccm;
          this.bike.stroke = res.data.stroke;
          this.bike.piston = res.data.piston;
          this.bike.year = res.data.year;
        });
    },
    putMaintenance(MtnId) {
      const path = `/api/maintenance/${MtnId}`;
      const payload = this.bike.operating_hours;
      axios.put(path, payload)
        .then(() => {
          this.getMaintenance();
        })
        .catch((error) => {
          console.log(error);
          this.getHistory();
        });
    },
  },
  created() {
    this.getMaintenance();
  },
};
</script>
