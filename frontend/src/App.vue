<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      hide-on-scroll
      dense
    >

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

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

    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>
