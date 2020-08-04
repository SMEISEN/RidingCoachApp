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
      <v-icon>
        mdi-home
      </v-icon>
    </v-btn>
    <v-btn
      value="Maintenance"
      to="/maintenance"
    >
      <v-icon>
        mdi-wrench
      </v-icon>
    </v-btn>
    <v-btn
      value="Spare Parts"
      to="/spareparts"
    >
      <v-icon>
        mdi-medical-bag
      </v-icon>
    </v-btn>
    <v-btn
      value="Training"
      to="/training"
    >
      <v-icon>
        mdi-racing-helmet
      </v-icon>
    </v-btn>
    <v-btn
      value="History"
      to="/history"
    >
      <v-icon>
        mdi-calendar-edit
      </v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default {
  name: 'TheBottomNavigation',
  data: () => ({
    current_page: null,
  }),
  watch: {
    current_page() {
      this.$emit('currentPage', this.current_page);
    },
  },
  created() {
    this.current_page = this.$route.name;
  },
  updated() {
  },
};
</script>

<style scoped>
.v-bottom-navigation {
  justify-content: center;
  overflow-x: auto;
}
</style>
