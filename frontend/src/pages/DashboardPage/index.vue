<template v-slot:default>
  <v-app>
    <v-container
      grid-list
      fluid
    >
      <v-row dense>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-row dense>
            <v-col cols="12">
              <v-card
                :key="bikeId +'/wear'"
                class="card-container"
              >
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
              v-if="$vuetify.breakpoint.name !== 'xs'"
              cols="12"
            >
              <v-card
                v-if="setup_array.length > 0"
                :key="bikeId +'/setup/sm+'"
                class="card-container"
              >
                <v-card-title>
                  <span class="headline">Bike Setup</span>
                </v-card-title>
                <DashboardSetupState
                  :setup-array="setup_array"
                />
              </v-card>
            </v-col>
          </v-row>
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-card
            :key="bikeId +'/maintenance'"
            class="card-container"
          >
            <v-card-title>
              <span class="headline">Upcoming maintenance</span>
            </v-card-title>
            <DashboardMaintenanceState
              :maintenance-next="maintenance_array"
            />
          </v-card>
        </v-col>
        <v-col
          v-if="$vuetify.breakpoint.name === 'xs'"
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-card
            v-if="setup_array.length > 0"
            :key="bikeId +'/setup/xs'"
            class="card-container"
          >
            <v-card-title>
              <span class="headline">Bike Setup</span>
            </v-card-title>
            <DashboardSetupState
              :setup-array="setup_array"
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
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
              tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero
              eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea.
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
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
              tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero
              eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea.
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
import DashboardWearState from './DashboardWearState.vue';
import DashboardMaintenanceState from './DashboardMaintenanceState.vue';
import DashboardSetupState from './DashboardSetupState.vue';

export default {
  name: 'Dashboard',
  metaInfo: {
    title: 'Dashboard',
  },
  components: {
    DashboardSetupState,
    DashboardMaintenanceState,
    DashboardWearState,
  },
  data: () => ({
    wear_object: {
      brakes_front: '',
      brakes_rear: '',
      tires: '',
      engine: '',
    },
    maintenance_array: [],
    setup_array: [],
  }),
  computed: {
    bikeString() {
      return `${this.$store.getters
        .getCurrentBikeManufacturer} ${this.$store.getters
        .getCurrentBikeModel} ${this.$store.getters
        .getCurrentBikeYear}`;
    },
    bikeId() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  created() {
    this.getWear();
    this.getMaintenance();
    this.getSetup();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'selectBike') {
        this.getWear();
        this.getMaintenance();
        this.getSetup();
      }
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
    getSetup() {
      const setupArray = this.$store.getters.getCurrentBikeSetup;
      if (setupArray !== null) {
        this.setup_array = setupArray.filter((i) => i.category === 'Suspension');
      } else {
        this.setup_array = [];
      }
    },
    getWear() {
      apiQueryMaintenance({
        bike_id: this.bikeId,
        interval_type: 'estimated wear',
      })
        .then((res) => {
          this.wear_object.brakes_front = res.data.Brakes[Object.keys(res.data.Brakes)[0]];
          this.wear_object.brakes_front.name = 'Front brake pads';
          this.wear_object.brakes_rear = res.data.Brakes[Object.keys(res.data.Brakes)[1]];
          this.wear_object.brakes_rear.name = 'Rear brake pads';
          this.wear_object.tires = res.data.Wheels[Object.keys(res.data.Wheels)[0]];
          this.wear_object.tires.name = 'Tires';
          this.wear_object.engine = res.data.Engine[Object.keys(res.data.Engine)[0]];
          this.wear_object.engine.name = 'Engine revision';
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    getMaintenance() {
      apiQueryMaintenance({
        bike_id: this.bikeId,
        interval_type: 'planned cycle',
      })
        .then((res) => {
          this.maintenance_array = this.structureMaintenanceNext(res.data);
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
