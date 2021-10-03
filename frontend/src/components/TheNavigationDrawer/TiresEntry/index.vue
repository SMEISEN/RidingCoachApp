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
    <TireDialog
      :tireArray="tire_array"
    />
  </div>
</template>

<script>
import TireDialog from './TireDialog.vue';
import { apiGetTire } from '../../api/TireApi';

export default {
  name: 'TheNavigationDrawerTires',
  components: {
    TireDialog,
  },
  data: () => ({
    tire_array: null
  }),
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
  created() {
    this.getTire();
  },
  methods: {
    getTire() {
      apiGetTire()
        .then((res) => {
              this.tire_array = res.data;
              console.log(this.tire_array);
        });
    },
    tireDialog() {
      this.tire_dialog = true;
    },
  },
};
</script>

<style scoped>

</style>
