<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row
        dense
        align="stretch"
      >
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-card class="card-container">
            <v-card-title>
              <span class="headerline">
                {{ bikeString }}
              </span>
            </v-card-title>
            <DashboardWearState
              :wear-object="wear_object"
            />
          </v-card>
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-card class="card-container">
            <v-card-title>
              <span class="headline">Upcoming maintenance</span>
            </v-card-title>
            <DashboardMaintenanceState
              :maintenance-next="maintenance_array"
            />
          </v-card>
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
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
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
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
import {
  processStateOfIntervalHours,
  processLeftIntervalHours,
} from '../../components/utils/DataProcessingUtils';
import { apiQueryMaintenance } from '../../components/api/MaintenanceApi';
import { apiGetBike } from '../../components/api/BikeApi';
import DashboardWearState from './DashboardWearState.vue';
import DashboardMaintenanceState from './DashboardMaintenanceState.vue';

export default {
  name: 'Dashboard',
  metaInfo: {
    title: 'Dashboard',
  },
  components: {
    DashboardMaintenanceState,
    DashboardWearState,
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
  computed: {
    bikeString() {
      return `${this.$store.getters
        .getCurrentBikeManufacturer} ${this.$store.getters
        .getCurrentBikeModel} ${this.$store.getters
        .getCurrentBikeYear}`;
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
              hours_left: processLeftIntervalHours(
                Object.values(helperList1)[i].operating_hours,
                Object.values(helperList1)[i].interval_amount,
                this.$store.getters.getCurrentBikeOperatingHours,
              ),
            };
            const state = {
              state: processStateOfIntervalHours(
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
      apiGetBike().then((res) => {
        this.bike_object = res.data;
      });
    },
    getWear() {
      apiQueryMaintenance({
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'estimated wear',
      }).then((res) => {
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
      apiQueryMaintenance({
        bike_id: this.$store.getters.getCurrentBikeId,
        interval_type: 'planned cycle',
      }).then((res) => {
        this.maintenance_array = this.structureMaintenanceNext(res.data);
      });
    },
  },
};
</script>
