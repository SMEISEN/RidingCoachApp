<template>
  <v-app>
    <v-card
      :height="0.88 * window_height"
      style="overflow-y:auto; overflow-x: hidden;"
    >
      <v-card-title class="pa-0">
        <SparepartsToolbar
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
            :spareparts-search.sync="spareparts_search"
          />
        </v-container>
      </v-card-text>
    </v-card>
  </v-app>
</template>

<script>
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
    spareparts_buttons: 0,
    window_height: 800,
  }),
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
    this.window_height = window.innerHeight;
  },
};
</script>

<style scoped>

</style>
