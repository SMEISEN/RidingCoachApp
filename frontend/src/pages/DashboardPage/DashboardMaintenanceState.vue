<template>
  <v-simple-table
    hide-default-header
    hide-default-footer
    dense
    height="95px"
  >
    <tbody>
    <tr v-for="(maintenance_object, index) in orderedMaintenance"
        v-bind:key="index + $store.getters.getCurrentBikeOperatingHours"
    >
      <td style="font-size: 12px">{{ maintenance_object.name }}</td>
      <td style="min-width: 120px;width: 120px;max-width: 120px">
        <LinearProgressIntervalHours
          :hours_latest="maintenance_object.operating_hours"
          :hours_interval="maintenance_object.interval_amount"
          :hours_current="$store.getters.getCurrentBikeOperatingHours"
        />
      </td>
    </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import _ from 'lodash';
import LinearProgressIntervalHours from '../../components/common/LinearProgressIntervalHours';

export default {
  name: 'DashboardMaintenanceState',
  props: {
    maintenance_next: {
      type: Array,
      required: true,
    },
  },
  components: {
    LinearProgressIntervalHours,
  },
  computed: {
    orderedMaintenance() {
      return _.orderBy(this.maintenance_next, 'hours_left', 'asc');
    },
  },
}
</script>

<style scoped>

</style>
