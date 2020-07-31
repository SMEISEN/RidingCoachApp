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
      <TheNavigationDrawer />
      <TheInfoSnackbar />
    </v-main>
  </v-app>
</template>

<script>
import TheNavigationTabs from './components/TheNavigationTabs/index.vue';
import TheNavigationDrawer from './components/TheNavigationDrawer/index.vue';
import TheInfoSnackbar from './components/TheInfoSnackbar/index.vue';
import { apiGetAllBikes } from './components/api/BikeApi';

export default {
  name: 'App',
  components: {
    TheInfoSnackbar,
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
      { rel: 'shortcut icon', type: 'image/svg', href: `${process.env.BASE_URL}rc-logo.svg` },
    ],
  },

  data: () => ({
    confirm_delete_dialog: false,
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
      apiGetAllBikes()
        .then((res) => {
          this.$store.commit('setAllBikes', res.data);
          if (this.$store.getters.getCurrentBikeId === null) {
            this.$store.commit('selectBike', res.data[0]);
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

<style>
  html { overflow-y: auto }
</style>
