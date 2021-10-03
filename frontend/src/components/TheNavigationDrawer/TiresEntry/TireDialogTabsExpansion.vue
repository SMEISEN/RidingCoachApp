<template>
  <v-expansion-panels
    v-model="tire_panel"
    multiple
  >
    <v-expansion-panel>
      <v-expansion-panel-header>Front</v-expansion-panel-header>
        <v-expansion-panel-content>
          <TireDialogTabsExpansionTable
            :tireArray="tires_front"
          />
        </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>Rear</v-expansion-panel-header>
        <v-expansion-panel-content>
          <TireDialogTabsExpansionTable
            :tireArray="tires_rear"
          />
          </v-expansion-panel-content>
      </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import TireDialogTabsExpansionTable from './TireDialogTabsExpansionTable.vue';

export default {
  name: 'TireDialogTabsExpansion',
  components: {
      TireDialogTabsExpansionTable,
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  computed: {
      tires_front() {
        return this.tireArray.filter((i) => i.axis === 'Front');
      },
      tires_rear() {
        return this.tireArray.filter((i) => i.axis === 'Rear');
      },
  },
  data: () => ({
    tire_panel: [0,1],
  }),
};
</script>

<style scoped>

</style>