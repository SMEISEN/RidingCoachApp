<template>
  <v-simple-table
    hide-default-header
    hide-default-footer
    dense
    :height="tableHeight"
  >
    <tbody>
      <tr
        v-for="(maintenance_object, index) in orderedMaintenance"
        :key="index + $store.getters.getCurrentBikeOperatingHours"
      >
        <td style="font-size: 12px">
          {{ maintenance_object.name }}
        </td>
        <td style="min-width: 120px;width: 120px;max-width: 120px">
          <LinearProgressMaintenanceInterval
            :intervalState="maintenance_object.interval_state"
            :intervalUnit="maintenance_object.interval_unit"
            :absoluteDigits="1"
            :relativeDigits="0"
          />
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import LinearProgressMaintenanceInterval from '../../components/common/LinearProgressMaintenanceInterval.vue';

export default {
  name: 'DashboardMaintenanceState',
  components: {
    LinearProgressMaintenanceInterval,
  },
  props: {
    maintenanceNext: {
      type: Array,
      required: true,
    },
  },
  computed: {
    orderedMaintenance() {
      return this._.orderBy(this.maintenanceNext, item => item.interval_state.absolute, 'asc');
    },
    tableHeight() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return '95px';
        case 'sm': return '256px';
        case 'md': return '256px';
        case 'lg': return '256px';
        case 'xl': return '800px';
        default: return 'undefined';
      }
    },
  },
};
</script>

<style scoped>

</style>
