<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row dense align="stretch">
        <v-col cols="12" xs="12" sm="6" md="6">
          <v-card class="card-container">
            <v-card-title>
              <span class="headerline">
                {{ $store.getters.getCurrentBikeManufacturer + ' ' +
                   $store.getters.getCurrentBikeModel + ' ' +
                   $store.getters.getCurrentBikeYear }}
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
                    :value="currentStateIntervalHours(category_object.operating_hours,
                                                      category_object.interval_amount,
                                                      $store.getters.getCurrentBikeOperatingHours)"
                    rounded>
                    <template v-slot="{ value }">
                      <span class="white--text">
                        {{ leftIntervalHours(category_object.operating_hours,
                                             category_object.interval_amount,
                                             $store.getters.getCurrentBikeOperatingHours) }} h /
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
        <v-col cols="12" xs="12" sm="6" md="6">
          <v-card class="card-container">
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
                <td style="font-size: 12px">{{ test.name }}</td>
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
        <v-col cols="12" xs="12" sm="6" md="6">
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">Recent training</span>
            </v-card-title>
            <v-card-text>
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
              invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
              accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
              sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
              sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
              aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
              rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
              amet.
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
      return Number.parseFloat(state.toPrecision(2));
    },
    leftIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      const HoursLeft = HoursLatest + HoursInterval - BikeHours;
      return Number.parseFloat(HoursLeft.toPrecision(2));
    },
    structureMaintenanceNext(data) {
      const helperList1 = [];
      for (let i = 0; i < Object.values(data).length; i += 1) {
        Object.assign(helperList1, Object.values(data)[i]);
      }
      const helperList2 = [];
      for (let i = 0; i < Object.values(helperList1).length; i += 1) {
        if (Object.values(helperList1)[i].operating_hours !== undefined) {
          if (Object.values(helperList1)[i].interval_unit === 'h') {
            const name = { name: Object.keys(helperList1)[i] };
            const entry = Object.values(helperList1)[i];
            const HoursLeft = {
              hours_left: this.leftIntervalHours(
                Object.values(helperList1)[i].operating_hours,
                Object.values(helperList1)[i].interval_amount,
                this.$store.getters.getCurrentBikeOperatingHours,
              ),
            };
            const state = {
              state: this.currentStateIntervalHours(
                Object.values(helperList1)[i].operating_hours,
                Object.values(helperList1)[i].interval_amount,
                this.$store.getters.getCurrentBikeOperatingHours,
              ),
            };
            helperList2.push(Object.assign(entry, name, HoursLeft, state));
          }
        }
      }
      return helperList2;
    },
    getBikeData() {
      const ApiPath = '/api/bike';
      axios.get(ApiPath).then((res) => {
        this.bike_dict = res.data;
      });
    },
    getWear() {
      const ApiPath = '/api/maintenance/query';
      const payload = {
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'estimated wear',
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
      const ApiPath = '/api/maintenance/query';
      const payload = {
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'planned cycle',
      };
      axios.post(ApiPath, payload).then((res) => {
        this.maintenance_next = this.structureMaintenanceNext(res.data);
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
