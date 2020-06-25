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
        :bike_array="bike_array"
        @updatedBike="updatedBike()"
      />
      <TheNavigationDrawerTraining
        :bike_array="bike_array"
      />
      <TheNavigationDrawerSpareParts/>
      <TheNavigationDrawerSettings/>
      <TheNavigationDrawerLogout/>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import TheNavigationDrawerBike from './BikeEntry';
import TheNavigationDrawerTraining from './TrainingEntry';
import TheNavigationDrawerSpareParts from './SparePartsEntry';
import TheNavigationDrawerSettings from './SettingsEntry';
import TheNavigationDrawerLogout from './LogoutEntry';


export default {
  name: 'TheNavigationDrawer',
  props: {
    bike_array: {
      type: Array,
      required: true,
    },
  },
  components: {
    TheNavigationDrawerBike,
    TheNavigationDrawerTraining,
    TheNavigationDrawerSpareParts,
    TheNavigationDrawerSettings,
    TheNavigationDrawerLogout,
  },
  computed: {
    navigation_drawer: {
      get() { return this.$store.getters.getNavigationDrawerState },
      set(value) { this.$store.commit('setNavigationDrawerState', value) }
    },
  },
  methods: {
    updatedBike() {
      this.$emit('updated');
    },
  },
  updated() {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
