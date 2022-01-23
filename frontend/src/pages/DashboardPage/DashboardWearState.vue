<template>
  <v-simple-table
    hide-default-header
    hide-default-footer
    dense
  >
    <tbody>
      <tr
        v-for="(wear_object, index) in wearObject"
        :key="index + $store.getters.getCurrentBikeOperatingHours"
      >
        <td>{{ wear_object.name }}</td>
        <td v-if="!Object.keys(wear_object).includes('operating_hours')" />
        <td
          v-else
          style="min-width: 120px;width: 120px;max-width: 120px"
        >
          <LinearProgressMaintenanceInterval
            :interval-state="wear_object.interval_state"
            :interval-unit="wear_object.interval_unit"
            :absolute-digitsto-precision="2"
            :relative-digits-to-fixed="0"
          />
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import LinearProgressMaintenanceInterval from '../../components/common/LinearProgressMaintenanceInterval.vue';

export default {
  name: 'DashboardWearState',
  components: {
    LinearProgressMaintenanceInterval,
  },
  props: {
    wearObject: {
      type: Object,
      required: true,
    },
  },
};
</script>
