<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      hide-on-scroll
      dense
    >

      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

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


      <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
      >
        <v-list
          nav
          dense
        >
          <v-list-item-group active-class="primary--text text--accent">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-motorbike</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Bike</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-settings</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Settings</v-list-item-title>
            </v-list-item>

          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  metaInfo: {
    titleTemplate: '%s | Riding Coach',
    meta: [
      { name: 'viewport', content: 'width=device-width' },
      { name: 'mobile-web-app-capable', content: 'yes' },
    ],
    link: [
      { rel: 'shortcut icon', type: 'image/png', href: '/rc-logo.png' },
    ],
  },

  data: () => ({
    drawer: false,
  }),
};
</script>
