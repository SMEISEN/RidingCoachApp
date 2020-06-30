<template>
  <v-app>
    <v-app-bar
      v-if="isAuthenticated"
      app
      color="primary"
      dark
      hide-on-scroll
      dense
    >
      <v-app-bar-nav-icon @click="onNavBarIcon()" />
      <TheNavigationTabs />
    </v-app-bar>
    <v-main>
      <router-view />
      <TheNavigationDrawer
        :bike-array="bike_list"
        @updated="getBike()"
      />
    </v-main>
  </v-app>
</template>

<script>
import TheNavigationTabs from './components/TheNavigationTabs/index.vue';
import TheNavigationDrawer from './components/TheNavigationDrawer/index.vue';
import { apiGetBike } from './components/api/BikeApi';

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
  created() {
    this.getBike();
  },
  updated() {
  },
  methods: {
    onNavBarIcon() {
      this.$store.commit('setNavigationDrawerState', true);
    },
    getBike() {
      apiGetBike().then((res) => {
        this.bike_list = res.data;
        if (this.$store.getters.getCurrentBikeId === null) {
          this.selectBike(0);
        }
      });
    },
  },
};
</script>

<style>
  html { overflow-y: auto }
</style>
