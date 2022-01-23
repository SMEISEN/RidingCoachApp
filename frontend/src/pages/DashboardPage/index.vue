<template>
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
        // update page if a new bike is selected
        initObject(this.wear_object, '');
        this.maintenance_array = [];
        this.setup_array = [];
        this.getWear();
        this.getMaintenance();
        this.getSetup();
      }
    });
  },
  methods: {
    /**
     * Gets the setup of the selected bike from the vuex store.
     */
    getSetup() {
      const setupArray = this.$store.getters.getCurrentBikeSetup;
      if (setupArray !== null) {
        this.setup_array = setupArray.filter((i) => i.category === 'Suspension');
      } else {
        this.setup_array = [];
      }
    },
    /**
     * Gets the maintenance items of interval type "estimated wear" and interval unit "h" for the
     * selected bike from the database and adds them to the wear object.
     */
    getWear() {
      apiQueryMaintenance({
        bike_id: this.bikeId,
        interval_type: 'estimated wear',
        interval_unit: 'h',
      })
        .then((res) => {
          if (Object.keys(res.data).length > 0) {
            [this.wear_object.brakes_front] = res.data.filter(
              (i) => i.name === 'Replace the brake pads of the front brake.',
            );
            this.wear_object.brakes_front.name = 'Front brake pads';
            [this.wear_object.brakes_rear] = res.data.filter(
              (i) => i.name === 'Replace the brake pads of the rear brake.',
            );
            this.wear_object.brakes_rear.name = 'Rear brake pads';
            [this.wear_object.tires] = res.data.filter(
              (i) => i.name === 'Replace tyres.',
            );
            this.wear_object.tires.name = 'Tires';
            [this.wear_object.engine] = res.data.filter(
              (i) => i.name === 'Engine revision.',
            );
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
    /**
     * Gets the maintenance items of interval type "planned cycle" and interval unit "h" for the
     * selected bike from the database and adds them to the maintenance array.
     */
    getMaintenance() {
      apiQueryMaintenance({
        bike_id: this.bikeId,
        interval_type: 'planned cycle',
        interval_unit: 'h',
      })
        .then((res) => {
          if (Object.keys(res.data).length > 0) {
            this.maintenance_array = res.data.filter(
              (i) => i.operating_hours !== undefined,
            );
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
