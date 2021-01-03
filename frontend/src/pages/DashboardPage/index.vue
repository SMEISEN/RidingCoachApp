<template v-slot:default>
  <v-app>
    <v-container fluid>
      <v-row dense>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-row dense>
            <v-col
              class="pt-0"
              cols="12"
            >
              <v-card
                :key="bikeId +'/wear'"
                class="card-container"
              >
                <v-card-title class="py-2">
                  <span class="headerline">
                    {{ bikeString }}
                  </span>
                  <v-spacer />
                  <span class="headerline">
                    {{ bikeHours + ' h' }}
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
                <v-card-title class="py-2">
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
          v-if="$vuetify.breakpoint.name !== 'xs'"
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-row dense>
            <v-col
              class="pt-0"
              cols="12"
            >
              <v-card
                :key="bikeId +'/maintenance'"
                class="card-container"
              >
                <v-card-title class="py-2">
                  <span class="headline">Upcoming maintenance</span>
                </v-card-title>
                <DashboardMaintenanceState
                  :maintenance-next="maintenance_array"
                />
              </v-card>
            </v-col>
            <v-col cols="12">
              <v-card class="card-container">
                <v-card-title class="py-2">
                  <span class="headline">Recent activity</span>
                </v-card-title>
                <DashboardTimeline />
              </v-card>
            </v-col>
          </v-row>
        </v-col>
        <v-col
          v-if="$vuetify.breakpoint.name === 'xs'"
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-card
            :key="bikeId +'/maintenance'"
            class="card-container"
          >
            <v-card-title class="py-2">
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
            <v-card-title class="py-2">
              <span class="headline">Bike Setup</span>
            </v-card-title>
            <DashboardSetupState
              :setup-array="setup_array"
            />
          </v-card>
        </v-col>
        <v-col
          v-if="$vuetify.breakpoint.name === 'xs'"
          cols="12"
        >
          <v-card class="card-container">
            <v-card-title class="py-2">
              <span class="headline">Recent activity</span>
            </v-card-title>
            <DashboardTimeline />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import { apiQueryMaintenance } from '../../components/api/MaintenanceApi';
import { initObject } from '../../components/utils/FromUtils';
import DashboardWearState from './DashboardWearState.vue';
import DashboardMaintenanceState from './DashboardMaintenanceState.vue';
import DashboardSetupState from './DashboardSetupState.vue';
import DashboardTimeline from './DashboardTimeline.vue';

export default {
  name: 'Dashboard',
  metaInfo: {
    title: 'Dashboard',
  },
  components: {
    DashboardTimeline,
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
    bikeHours() {
      return `${this.$store.getters.getCurrentBikeOperatingHours}`;
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
        initObject(this.wear_object, '');
        this.maintenance_array = [];
        this.setup_array = [];
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
          const name = { name: Object.keys(helperList1)[i] };
          helperList2.push(Object.assign(
            name,
            Object.values(helperList1)[i],
          ));
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
        interval_unit: 'h',
      })
        .then((res) => {
          if (Object.keys(res.data).length > 0) {
            this.wear_object.brakes_front = res.data.Brakes[Object.keys(res.data.Brakes)[0]];
            this.wear_object.brakes_front.name = 'Front brake pads';
            this.wear_object.brakes_rear = res.data.Brakes[Object.keys(res.data.Brakes)[1]];
            this.wear_object.brakes_rear.name = 'Rear brake pads';
            this.wear_object.tires = res.data.Wheels[Object.keys(res.data.Wheels)[0]];
            this.wear_object.tires.name = 'Tires';
            this.wear_object.engine = res.data.Engine[Object.keys(res.data.Engine)[0]];
            this.wear_object.engine.name = 'Engine revision';
          }
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
        interval_unit: 'h',
      })
        .then((res) => {
          if (Object.keys(res.data).length > 0) {
            this.maintenance_array = this.structureMaintenanceNext(res.data);
          }
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
