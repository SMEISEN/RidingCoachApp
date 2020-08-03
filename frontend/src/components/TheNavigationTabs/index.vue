<template>
  <v-tabs
    v-model="current_tab"
    grow
    right
    dark
    background-color="primary"
  >
    <v-tabs-slider color="accent" />
    <v-tab to="/dashboard">
      <v-icon>
        mdi-home
      </v-icon>
    </v-tab>
    <v-tab to="/maintenance">
      <v-icon>
        mdi-view-list
      </v-icon>
    </v-tab>
    <v-tab to="/history">
      <v-icon>
        mdi-calendar
      </v-icon>
    </v-tab>
  </v-tabs>
</template>

<script>
export default {
  name: 'TheNavigationTabs',
  data: () => ({
    current_tab: null,
  }),
  watch: {
    current_tab() {
      let pageTitle = 'Error: Page title unknown!';
      if (this.current_tab === '/dashboard') {
        pageTitle = 'Dashboard';
      } else if (this.current_tab === '/maintenance') {
        pageTitle = 'Maintenance';
      } else if (this.current_tab === '/history') {
        pageTitle = 'History';
      }
      this.$emit('currentPage', pageTitle);
    },
  },
  created() {
  },
  updated() {
  },
};
</script>

<style scoped>

</style>
