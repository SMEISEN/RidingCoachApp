<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      hide-on-scroll
      dense
      v-if="isAuthenticated"
    >
      <v-app-bar-nav-icon @click="onNavBarIcon()"/>
      <TheNavigationTabs/>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
      <TheNavigationDrawer
        :bike_array="bike_list"
        @updated="getBikeData()"
      />

    </v-content>
  </v-app>
</template>

<script>
import TheNavigationTabs from './components/TheNavigationTabs';
import TheNavigationDrawer from './components/TheNavigationDrawer';
import {BikeApi} from './components/api/BikeApi';

export default {
  name: 'App',
  components: {
    TheNavigationTabs,
    TheNavigationDrawer,
  },
  metaInfo: {
    titleTemplate: '%s | Riding Coach',
    meta: [
      { name: 'viewport', content: 'width=device-width' },
      { name: 'mobile-web-app-capable', content: 'yes' },
    ],
    link: [
      { rel: 'shortcut icon', type: 'image/svg', href: '/rc-logo.svg' },
    ],
  },

  data: () => ({
    confirm_delete_dialog: false,
    bike_list: [],
    active_tr: false,
    edit: false,
  }),
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    onNavBarIcon() {
      this.$store.commit('setNavigationDrawerState', true);
    },
    getBikeData() {
      BikeApi.getBike().then((res) => {
        this.bike_list = res.data;
        if (this.$store.getters.getCurrentBikeId === null) {
          this.selectBike(0);
      }});
    },
  },
  created() {
    this.getBikeData();
  },
  updated() {
  },
};
</script>

<style>
  html { overflow-y: auto }
</style>
