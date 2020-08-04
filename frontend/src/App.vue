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
      <v-avatar
        tile
        size="30px"
      >
        <v-img
          contain
          :src="'/favicon.svg'"
          alt="Riding Coach"
        />
      </v-avatar>
      <v-toolbar-title class="pl-4">
        {{ current_tab }}
      </v-toolbar-title>
      <v-spacer />
      <v-app-bar-nav-icon @click="onNavBarIcon()" />
    </v-app-bar>
    <TheNavigationDrawer />
    <TheBottomNavigation
      v-if="isAuthenticated"
      @currentPage="setPage"
    />
    <TheFooter />
    <v-main>
      <router-view />
      <TheInfoSnackbar />
    </v-main>
  </v-app>
</template>

<script>
import TheNavigationDrawer from './components/TheNavigationDrawer/index.vue';
import TheInfoSnackbar from './components/TheInfoSnackbar/index.vue';
import TheBottomNavigation from './components/TheBottomNavigation/index.vue';
import TheFooter from './components/TheFooter/index.vue';
import { apiGetAllBikes } from './components/api/BikeApi';

export default {
  name: 'App',
  components: {
    TheBottomNavigation,
    TheFooter,
    TheInfoSnackbar,
    TheNavigationDrawer,
  },
  metaInfo: {
    titleTemplate: '%s | Riding Coach',
    meta: [
      {
        name: 'viewport',
        content: 'width=device-width',
      },
      {
        name: 'mobile-web-app-capable',
        content: 'yes',
      },
    ],
    link: [
      {
        rel: 'shortcut icon',
        type: 'image/svg',
        href: 'favicon.svg',
      },
    ],
  },
  data: () => ({
    confirm_delete_dialog: false,
    active_tr: false,
    edit: false,
    current_tab: 'test',
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
    setPage(value) {
      this.current_tab = value;
    },
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
