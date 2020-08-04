<template>
  <v-navigation-drawer
    v-model="navigation_drawer"
    app
    absolute
    right
    style="position:fixed; top:48px; left:0"
    temporary
    width="auto"
    :height="window_height - 105"
  >
    <v-list>
      <TheNavigationDrawerBike />
      <TheNavigationDrawerTraining />
      <TheNavigationDrawerSpareParts />
      <TheNavigationDrawerSettings />
      <TheNavigationDrawerLogout />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import TheNavigationDrawerBike from './BikeEntry/index.vue';
import TheNavigationDrawerTraining from './TrainingEntry/index.vue';
import TheNavigationDrawerSpareParts from './SparePartsEntry/index.vue';
import TheNavigationDrawerSettings from './SettingsEntry/index.vue';
import TheNavigationDrawerLogout from './LogoutEntry/index.vue';

export default {
  name: 'TheNavigationDrawer',
  components: {
    TheNavigationDrawerBike,
    TheNavigationDrawerTraining,
    TheNavigationDrawerSpareParts,
    TheNavigationDrawerSettings,
    TheNavigationDrawerLogout,
  },
  data: () => ({
    window_height: window.innerHeight,
  }),
  computed: {
    navigation_drawer: {
      get() {
        return this.$store.getters.getNavigationDrawerState;
      },
      set(value) {
        this.$store.commit('setNavigationDrawerState', value);
      },
    },
    bike_array: {
      get() {
        return this.$store.getters.getAllBikes;
      },
      set(value) {
        this.$store.commit('setAllBikes', value);
      },
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
  },
};
</script>

<style scoped>

</style>
