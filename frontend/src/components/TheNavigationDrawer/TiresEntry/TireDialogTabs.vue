<template>
  <v-tabs
    fixed-tabs
    background-color="secondary"
    dark
  >
    <v-tab>
      Slick
    </v-tab>
    <v-tab-item>
      <TireDialogTabsExpansion
        :tire-array="tires_slick"
        :tire-category="'Slick'"
        @refreshTires="$emit('refreshTires')"
      />
    </v-tab-item>
    <v-tab>
      Rain
    </v-tab>
    <v-tab-item>
      <TireDialogTabsExpansion
        :tire-array="tires_rain"
        :tire-category="'Rain'"
        @refreshTires="$emit('refreshTires')"
      />
    </v-tab-item>
  </v-tabs>
</template>

<script>
import TireDialogTabsExpansion from './TireDialogTabsExpansion.vue';

export default {
  name: 'TireDialogTabs',
  components: {
    TireDialogTabsExpansion,
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  computed: {
    /**
     * Switches to the slick tires.
     * @returns {array} array of slick tires of the selected bike
     */
    tires_slick() {
      return this.tireArray.filter((i) => i.category === 'Slick');
    },
    /**
     * Switches to the rain tires.
     * @returns {array} array of rain tires of the selected bike
     */
    tires_rain() {
      return this.tireArray.filter((i) => i.category === 'Rain');
    },
  },
};
</script>
