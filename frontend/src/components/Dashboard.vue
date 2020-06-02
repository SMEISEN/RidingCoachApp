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
              <v-card class="card-container" height="170px">
                <v-card-title>
                  <span class="headline">Upcoming maintenance</span>
                </v-card-title>
                <v-simple-table
                  hide-default-header
                  hide-default-footer
                  dense
                  height="95px"
                >
                  <tbody>
                  <tr v-for="(test, index) in orderedUsers"
                      v-bind:key="index">
                    <td>{{ test.name }}</td>
                    <td style="min-width: 120px;width: 120px;max-width: 120px">
                      <v-progress-linear
                        color="primary"
                        background-color="accent"
                        height="22"
                        :value="test.state"
                        rounded>
                        <template v-slot="{ value }">
                          <span class="white--text">
                            {{ test.hours_left }} h /
                            {{ Math.ceil(value) }} %
                          </span>
                        </template>
                      </v-progress-linear>
                    </td>
                  </tr>
                  </tbody>
                </v-simple-table>
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
import _ from 'lodash';

export default {
  name: 'Dashboard',
  metaInfo: {
    title: 'Dashboard',
  },
  data: () => ({
    bike_dict: {},
    wear_dict: {
      brakes_front: '',
      brakes_rear: '',
      tires: '',
      engine: '',
    },
    maintenance_next: [],
  }),
  computed: {
    orderedUsers() {
      return _.orderBy(this.maintenance_next, 'hours_left');
    },
  },
  methods: {
    currentStateIntervalHours(Latest, Interval, Current) {
      const state = ((Latest + Interval - Current) / Interval) * 100;
      return state.toPrecision(2);
    },
    leftIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      const HoursLeft = HoursLatest + HoursInterval - BikeHours;
      return HoursLeft.toPrecision(2);
    },
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
        field: 'interval_type',
        op: '=',
        value: 'planned cycle',
      };
      axios.post(ApiPath, payload).then((res) => {
        for (let i = 0; i < Object.values(res.data).length; i += 1) {
          Object.assign(this.maintenance_next, Object.values(res.data)[i]);
        }
        const test = [];
        for (let i = 0; i < Object.values(this.maintenance_next).length; i += 1) {
          if (Object.values(this.maintenance_next)[i].operating_hours !== undefined) {
            if (Object.values(this.maintenance_next)[i].interval_unit === 'h') {
              const name = { name: Object.keys(this.maintenance_next)[i] };
              const entry = Object.values(this.maintenance_next)[i];
              const HoursLeft = {
                hours_left: this.leftIntervalHours(
                  Object.values(this.maintenance_next)[i].operating_hours,
                  Object.values(this.maintenance_next)[i].interval_amount,
                  this.bike_dict.operating_hours,
                ),
              };
              const state = {
                state: this.currentStateIntervalHours(
                  Object.values(this.maintenance_next)[i].operating_hours,
                  Object.values(this.maintenance_next)[i].interval_amount,
                  this.bike_dict.operating_hours,
                ),
              };
              test.push(Object.assign(entry, name, HoursLeft, state));
            }
          }
        }
        this.maintenance_next = test;
      });
    },
  },
  created() {
    this.getBikeData();
    this.getWear();
    this.getMaintenance();
  },
  updated() {
  },
};
</script>
