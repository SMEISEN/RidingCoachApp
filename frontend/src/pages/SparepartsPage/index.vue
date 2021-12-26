<template>
  <v-app>
    <v-card
      :height="0.88 * window_height"
      style="overflow-y:auto; overflow-x: hidden;"
    >
      <v-card-title class="pa-0">
        <SparepartsToolbar
          :bike-modules="bike_modules"
          :spareparts-buttons.sync="spareparts_buttons"
        />
      </v-card-title>
      <v-card-text>
        <v-container class="mt-n2">
          <v-text-field
            v-model="spareparts_search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          />
        </v-container>
        <v-container>
          <SparepartsTable
            :sparepart-items="sparepart_array"
            :spareparts-search.sync="spareparts_search"
            :bike-modules="bike_modules"
            @refreshSpareParts="getSpareparts"
          />
        </v-container>
      </v-card-text>
    </v-card>
  </v-app>
</template>

<script>
import { apiQuerySpareparts } from '../../components/api/SparepartApi';
import SparepartsToolbar from './SparepartsToolbar.vue';
import SparepartsTable from './SparepartsTable.vue';

export default {
  name: 'Spareparts',
  metaInfo: {
    title: 'Spare Parts',
  },
  components: {
    SparepartsToolbar,
    SparepartsTable,
  },
  data: () => ({
    spareparts_search: '',
    spareparts_buttons: null,
    window_height: 800,
    sparepart_array: [],
    bike_modules: [
      'Attachments',
      'Brakes',
      'Carburetor',
      'Engine',
      'Suspension',
      'Wheels',
    ],
  }),
  computed: {
    current_module() {
      switch (this.spareparts_buttons) {
        case 0:
          return 'Attachments';
        case 1:
          return 'Brakes';
        case 2:
          return 'Carburetor';
        case 3:
          return 'Engine';
        case 4:
          return 'Suspension';
        case 5:
          return 'Wheels';
        default:
          return null;
      }
    },
  },
  watch: {
    spareparts_buttons() {
      this.getSpareparts();
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
    this.window_height = window.innerHeight;
    this.getSpareparts();
  },
  methods: {
    /**
     * Queries the spare part items for the selected module.
     */
    getSpareparts() {
      const payload = { module: this.current_module };
      apiQuerySpareparts(payload)
        .then((res) => {
          this.sparepart_array = res.data;
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

<style scoped>

</style>
