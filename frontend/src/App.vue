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
    current_bike_id() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  created() {
    this.getBike();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'selectBike') {
        this.getBike();
      }
    });
  },
  updated() {
  },
  methods: {
    /**
     * Highlights the current page in the bottom navigation.
     * @param {string} value Name of the current page
     */
    setPage(value) {
      this.current_tab = value;
    },
    /**
     * Opens the navigation drawer.
     */
    onNavBarIcon() {
      this.$store.commit('setNavigationDrawerState', true);
    },
    /**
     * Get all bikes and store them to the vuex store. If there is no bike selected, select the
     * first bike in the array. Store the information of the selected bike.
     */
    getBike() {
      apiGetAllBikes()
        .then((res) => {
          this.$store.commit('setAllBikes', res.data);
          if (this.current_bike_id === null) {
            const currentBikeData = res.data[0];
            this.$store.commit('updateCurrentBike', currentBikeData);
          } else {
            const currentBikeData = res.data.find((o) => o.bike_id === this.current_bike_id);
            this.$store.commit('updateCurrentBike', currentBikeData);
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
