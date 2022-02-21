<template>
  <v-bottom-navigation
    v-model="current_page"
    app
    grow
    dark
    background-color="primary"
  >
    <v-btn
      class="bottom-navigation-btn"
      value="Dashboard"
      to="/dashboard"
    >
      <span
        :style="calculateFontSize"
      >
        Dashboard
      </span>
      <v-icon>
        mdi-home
      </v-icon>
    </v-btn>
    <v-btn
      class="bottom-navigation-btn"
      value="Maintenance"
      to="/maintenance"
    >
      <span
        :style="calculateFontSize"
      >
        Maintenance
      </span>
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
      class="bottom-navigation-btn"
      value="Spare Parts"
      to="/spareparts"
    >
      <span
        :style="calculateFontSize"
      >
        Spare Parts
      </span>
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
      class="bottom-navigation-btn"
      value="Training"
      to="/training"
    >
      <span
        :style="calculateFontSize"
      >
        Training
      </span>
      <v-icon>
        mdi-racing-helmet
      </v-icon>
    </v-btn>
    <v-btn
      class="bottom-navigation-btn"
      value="History"
      to="/history"
    >
      <span
        :style="calculateFontSize"
      >
        History
      </span>
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
    window_width: null,
    current_page: null,
    maintenance_warnings: 0,
    sparepart_warnings: 0,
  }),
  computed: {
    currentBikeId() {
      return this.$store.getters.getCurrentBikeId;
    },
    calculateFontSize() {
      if (this.window_width < 375) {
        return 'fontSize:0px';
      }
      if (this.window_width >= 375 && this.window_width < 450) {
        return `fontSize:${(this.window_width - 375) * 0.05 + 9}px`;
      }
      return 'fontSize:12px';
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
      if (mutation.type === 'setCurrentOperatingHours'
        || mutation.type === 'selectBike'
        || mutation.type === 'setHistoryId'
      ) {
        this.getMaintenanceWarnings();
      }
    });
  },
  updated() {
    this.window_width = window.innerWidth;
  },
  methods: {
    /**
     * Get the spare part warnings from the database, i.e., spare parte where the current stock is
     * smaller than the minimal stock.
     */
    getSparepartWarnings() {
      apiGetSparepartWarnings().then((res) => {
        this.sparepart_warnings = res.data.warnings;
      });
    },
    /**
     * Get the maintenance warnings from the database, i.e., maintenance items where maintenance
     * needs to be done.
     */
    getMaintenanceWarnings() {
      apiGetMaintenanceWarnings(this.currentBikeId).then((res) => {
        this.maintenance_warnings = res.data.warnings;
      });
    },
  },
};
</script>

<style scoped>
.v-btn.bottom-navigation-btn {
  min-width: 0 !important;
}
</style>
