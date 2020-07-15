<template>
  <v-navigation-drawer
    v-model="navigation_drawer"
    absolute
    style="position:fixed; top:48px; left:0;"
    temporary
    width="auto"
  >
    <v-list>
      <TheNavigationDrawerBike
        :bike-array.sync="bike_array"
      />
      <TheNavigationDrawerTraining
        :bike-array="bike_array"
      />
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
  props: {
    bikeArray: {
      type: Array,
      required: true,
    },
  },
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
        return this.bikeArray;
      },
      set(value) {
        this.$emit('update:bikeArray', value);
      },
    },
  },
  updated() {
  },
  created() {
  },
};
</script>

<style scoped>

</style>
