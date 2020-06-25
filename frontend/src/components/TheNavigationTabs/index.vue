<template>
  <v-tabs
    grow
    right
    dark
  >
    <v-tabs-slider color="accent"></v-tabs-slider>

    <v-tab to="/dashboard">
      Dashboard
    </v-tab>
    <v-tab to="/maintenance">
      Maintenance
    </v-tab>
    <v-tab to="/history">
      History
    </v-tab>

  </v-tabs>
</template>

<script>
export default {
  name: 'TheNavigationTabs',
}
</script>

<style scoped>

</style>
