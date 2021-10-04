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
      :tire-array="tire_array"
      @saveButtonClicked="getTires()"
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
    tire_array: [],
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
    this.getTires();
  },
  methods: {
    getTires() {
      apiGetTire()
        .then((res) => {
              this.tire_array = res.data;
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
