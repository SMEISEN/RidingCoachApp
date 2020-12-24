<template>
  <v-bottom-navigation
    v-model="current_page"
    app
    grow
    dark
    background-color="primary"
  >
    <v-btn
      icon
      value="Dashboard"
      to="/dashboard"
    >
      <span>Dashboard</span>
      <v-icon>
        mdi-home
      </v-icon>
    </v-btn>
    <v-btn
      value="Maintenance"
      to="/maintenance"
    >
      <span>Maintenance</span>
      <v-badge
        v-if="maintenance_warnings > 0"
        color="red"
        :content="maintenance_warnings"
        overlap
      >
        <v-icon>
          mdi-wrench
        </v-icon>
      </v-badge>
      <v-icon v-else>
        mdi-wrench
      </v-icon>
    </v-btn>
    <v-btn
      value="Spare Parts"
      to="/spareparts"
    >
      <span>Spare Parts</span>
      <v-badge
        v-if="sparepart_warnings > 0"
        color="red"
        :content="sparepart_warnings"
        overlap
      >
        <v-icon>
          mdi-medical-bag
        </v-icon>
      </v-badge>
      <v-icon v-else>
        mdi-medical-bag
      </v-icon>
    </v-btn>
    <v-btn
      value="Training"
      to="/training"
    >
      <span>Training</span>
      <v-icon>
        mdi-racing-helmet
      </v-icon>
    </v-btn>
    <v-btn
      value="History"
      to="/history"
    >
      <span>History</span>
      <v-icon>
        mdi-calendar-edit
      </v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
import {
  apiGetSparepartWarnings,
} from '../api/SparepartApi';
import {
  apiGetMaintenanceWarnings,
} from '../api/MaintenanceApi';

export default {
  name: 'TheBottomNavigation',
  data: () => ({
    current_page: null,
    maintenance_warnings: 0,
    sparepart_warnings: 0,
  }),
  computed: {
    currentBikeId() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  watch: {
    current_page() {
      this.$emit('currentPage', this.current_page);
    },
  },
  created() {
    this.current_page = this.$route.name;
    this.getSparepartWarnings();
    this.getMaintenanceWarnings();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setSparepartId' || mutation.type === 'selectBike') {
        this.getSparepartWarnings();
      }
    });
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'getCurrentBikeOperatingHours'
        || mutation.type === 'selectBike'
        || mutation.type === 'setHistoryId'
      ) {
        this.getMaintenanceWarnings();
      }
    });
  },
  updated() {
  },
  methods: {
    getSparepartWarnings() {
      apiGetSparepartWarnings().then((res) => {
        this.sparepart_warnings = res.data.warnings;
      });
    },
    getMaintenanceWarnings() {
      apiGetMaintenanceWarnings(this.currentBikeId).then((res) => {
        this.maintenance_warnings = res.data.warnings;
      });
    },
  },
};
</script>

<style scoped>

</style>
