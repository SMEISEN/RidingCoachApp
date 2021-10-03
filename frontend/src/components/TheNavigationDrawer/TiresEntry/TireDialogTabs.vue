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
      <TireDialogTabsExpansion />
    </v-tab-item>
    <v-tab>
      Rain
    </v-tab>
    <v-tab-item>
      <TireDialogTabsExpansion />
    </v-tab-item>
  </v-tabs>
</template>

<script>
import TireDialogTabsExpansion from './TireDialogTabsExpansion.vue';

export default {
  name: 'TireDialogTabs',
  components: {
    TireDialogTabsExpansion
  },
  data: () => ({
  }),
};
</script>

<style scoped>

</style>
