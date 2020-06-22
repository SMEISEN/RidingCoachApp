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
            <DashboardWearState
              :wear_object="wear_object"
            />
          </v-card>
        </v-col>
        <v-col cols="12" xs="12" sm="6" md="6">
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">Upcoming maintenance</span>
            </v-card-title>
            <DashboardMaintenanceState
              :maintenance_next="maintenance_array"
            />
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
        <v-col cols="12" xs="12" sm="6" md="6">
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">Spare parts</span>
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
import DashboardWearState from './DashboardWearState';
import DashboardMaintenanceState from './DashboardMaintenanceState';
import {DataProcessingUtils} from '../../components/utils/DataProcessingUtils';
import {MaintenanceApi} from '../../components/api/MaintenanceApi';
import {BikeApi} from '../../components/api/BikeApi';

export default {
  name: 'Dashboard',
  metaInfo: {
    title: 'Dashboard',
  },
  components: {
    DashboardMaintenanceState,
    DashboardWearState
  },
  data: () => ({
    bike_object: {},
    wear_object: {
      brakes_front: '',
      brakes_rear: '',
      tires: '',
      engine: '',
    },
    maintenance_array: [],
  }),
  methods: {
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
              hours_left: DataProcessingUtils.processLeftIntervalHours(
                Object.values(helperList1)[i].operating_hours,
                Object.values(helperList1)[i].interval_amount,
                this.$store.getters.getCurrentBikeOperatingHours,
              ),
            };
            const state = {
              state: DataProcessingUtils.processStateOfIntervalHours(
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
      BikeApi.getBike().then((res) => this.bike_object = res.data);
    },
    getWear() {
      MaintenanceApi.queryMaintenance({
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'estimated wear'}).then((res) => {
          this.wear_object.brakes_front = res.data.Brakes[Object.keys(res.data.Brakes)[0]];
          this.wear_object.brakes_front.name = 'Front brake pads';
          this.wear_object.brakes_rear = res.data.Brakes[Object.keys(res.data.Brakes)[1]];
          this.wear_object.brakes_rear.name = 'Rear brake pads';
          this.wear_object.tires = res.data.Wheels[Object.keys(res.data.Wheels)[0]];
          this.wear_object.tires.name = 'Tires';
          this.wear_object.engine = res.data.Motor[Object.keys(res.data.Motor)[0]];
          this.wear_object.engine.name = 'Engine revision';
      });
    },
    getMaintenance() {
      MaintenanceApi.queryMaintenance({
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'planned cycle'}).then((res) => {
        this.maintenance_array = this.structureMaintenanceNext(res.data);
      });
    },
  },
  created() {
    this.getBikeData();
    this.getWear();
    this.getMaintenance();
    this.$store.subscribe(() => {
      this.getBikeData();
      this.getWear();
      this.getMaintenance();
    });
  },
  updated() {
  },
};
</script>
