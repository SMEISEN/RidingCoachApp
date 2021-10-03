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
        :tireArray="tires_slick"
      />
    </v-tab-item>
    <v-tab>
      Rain
    </v-tab>
    <v-tab-item>
      <TireDialogTabsExpansion
        :tireArray="tires_rain"
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
