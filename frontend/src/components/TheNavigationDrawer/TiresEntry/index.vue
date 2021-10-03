<template>
  <div>
    <v-list-item @click="tireDialog">
      <v-list-item-icon>
        <v-icon>
          mdi-sync
        </v-icon>
      </v-list-item-icon>
      <v-list-item-title>
        Tires
      </v-list-item-title>
    </v-list-item>
    <TireDialog/>
  </div>
</template>

<script>
import TireDialog from './TireDialog.vue';

export default {
  name: 'TheNavigationDrawerTires',
  components: {
    TireDialog,
  },
  computed: {
    tire_dialog: {
      get() {
        return this.$store.getters.getTireDialogState;
      },
      set(value) {
        this.$store.commit('setTireDialogState', value);
      },
    },
  },
  methods: {
    tireDialog() {
      this.tire_dialog = true;
    },
  },
};
</script>

<style scoped>

</style>
