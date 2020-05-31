<template v-slot:default>
  <v-app>
    <v-flex>
      <v-layout wrap>
        <v-container fluid>
          <v-row dense>
            <v-col cols="12" xs="12" sm="6" md="6">
              <v-card class="card-container" height="170px">
                <v-card-title>
                  <span class="headerline">
                    {{ bike_dict.manufacturer + ' ' + bike_dict.model + ' ' + bike_dict.year }}
                  </span>
                </v-card-title>
                <v-simple-table
                  hide-default-header
                  hide-default-footer
                  dense
                >
                  <tbody>
                  <tr v-for="(category_object, category_name) in wear_dict"
                      v-bind:key="category_name">
                    <td>{{ category_object.name }}</td>
                    <td v-if="!Object.keys(category_object).includes('operating_hours')"></td>
                    <td v-else style="min-width: 120px;width: 120px;max-width: 120px">
                      <v-progress-linear
                        color="primary"
                        background-color="accent"
                        height="22"
                        :value="(category_object.operating_hours +
                        category_object.interval_amount -
                        bike_dict.operating_hours) / category_object.interval_amount * 100"
                        rounded>
                        <template v-slot="{ value }">
                          <span class="white--text">
                            {{ category_object.operating_hours +
                            category_object.interval_amount -
                            bike_dict.operating_hours }} h / {{ Math.ceil(value) }} %
                          </span>
                        </template>
                      </v-progress-linear>
                    </td>
                  </tr>
                  </tbody>
                </v-simple-table>
              </v-card>
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="6">
              <v-card class="card-container" height="280px">
                <v-card-title>
                  <span class="headline">Upcoming maintenance</span>
                  <v-data-table
                    hide-default-header
                    hide-default-footer
                  >
                  </v-data-table>
                  <tbody>
                  <tr v-for="(index, maintenance) in maintenance_next" v-bind:key="index">
                    <td>{{ maintenance.name }}</td>
                    <td>
                      <v-progress-linear
                        color="primary"
                        background-color="accent"
                        height="22"
                        :value="(maintenance.hours_last +
                        bike_dict.operating_hours)
                        / maintenance.hours_interval * 100"
                        rounded>
                        <template v-slot="{ value }">
                          <span class="white--text">
                            {{ maintenance.hours_last +
                            maintenance.hours_interval -
                            bike_dict.operating_hours }} h / {{ Math.ceil(value) }} %
                          </span>
                        </template>
                      </v-progress-linear>
                    </td>
                  </tr>
                  </tbody>
                </v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-layout>
    </v-flex>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data: () => ({
    bike_dict: {},
    wear_dict: {
      brakes_front: '',
      brakes_rear: '',
      tires: '',
      engine: '',
    },
    maintenance_next: {
      next_1: '',
      next_2: '',
      next_3: '',
      next_4: '',
      next_5: '',
    },
  }),
  methods: {
    getBikeData() {
      const ApiPath = '/api/bike';
      axios.get(ApiPath).then((res) => {
        this.bike_dict = res.data;
      });
    },
    getWear() {
      const ApiPath = '/api/maintenance/search';
      const payload = {
        field: 'interval_type',
        op: '=',
        value: 'estimated wear',
      };
      axios.post(ApiPath, payload).then((res) => {
        this.wear_dict.brakes_front = res.data.Brakes[Object.keys(res.data.Brakes)[0]];
        this.wear_dict.brakes_front.name = 'Front brake pads';
        this.wear_dict.brakes_rear = res.data.Brakes[Object.keys(res.data.Brakes)[1]];
        this.wear_dict.brakes_rear.name = 'Rear brake pads';
        this.wear_dict.tires = res.data.Wheels[Object.keys(res.data.Wheels)[0]];
        this.wear_dict.tires.name = 'Tires';
        this.wear_dict.engine = res.data.Motor[Object.keys(res.data.Motor)[0]];
        this.wear_dict.engine.name = 'Engine revision';
      });
    },
    getMaintenance() {
      const ApiPath = '/api/maintenance/search';
      const payload = {
        field: 'interval_unit',
        op: '=',
        value: 'h',
      };
      axios.post(ApiPath, payload).then((res) => {
        console.log(res);
      });
    },
  },
  created() {
    this.getBikeData();
    this.getWear();
    this.getMaintenance();
  },
};
</script>
