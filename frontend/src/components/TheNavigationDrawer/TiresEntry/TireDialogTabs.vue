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
        :tire-category="'slick'"
        @refreshTires="$emit('refreshTires')"
      />
    </v-tab-item>
    <v-tab>
      Rain
    </v-tab>
    <v-tab-item>
      <TireDialogTabsExpansion
        :tire-array="tires_rain"
        :tire-category="'rain'"
        @refreshTires="$emit('refreshTires')"
      />
    </v-tab-item>
  </v-tabs>
</template>

<script>
import TireDialogTabsExpansion from './TireDialogTabsExpansion.vue';

export default {
  name: 'TireDialogTabs',
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  components: {
    TireDialogTabsExpansion
  },
  computed: {
    tires_slick() {
      return this.tireArray.filter((i) => i.category === 'Slick');
    },
    tires_rain() {
      return this.tireArray.filter((i) => i.category === 'Rain');
    },
  },
  data: () => ({
  }),
};
</script>

<style scoped>

</style>
