<template>
  <v-simple-table
    dense
    fixed-header
    height="300px"
  >
    <thead>
      <tr>
        <th
          class="text-left"
          style="min-width: 120px"
        >
          Name
        </th>
        <th
          class="text-left"
          style="min-width: 120px;width: 120px;max-width: 120px"
        >
          State
        </th>
        <th
          class="button"
          style="min-width: 120px;width: 120px;max-width: 120px"
        />
        <th
          class="text-left"
          style="min-width: 80px;width: 80px;max-width: 80px"
        >
          Interval
        </th>
        <th
          class="text-left"
          style="width: 145px"
        >
          Date
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="maintenance_object in sort_maintenance(maintenanceEntries)"
        :key="maintenance_object.maintenance_id"
      >
        <td style="font-size: 12px">
          {{ maintenance_object.name }}
        </td>
        <td v-if="!Object.keys(maintenance_object).includes('operating_hours')" />
        <td v-else-if="maintenance_object.interval_unit === 'a'">
          <LinearProgressMaintenanceInterval
            :intervalState="maintenance_object.interval_state"
            :intervalUnit="maintenance_object.interval_unit"
            :absoluteDigits="0"
            :relativeDigits="0"
          />
        </td>
        <td v-else>
          <LinearProgressMaintenanceInterval
            :intervalState="maintenance_object.interval_state"
            :intervalUnit="maintenance_object.interval_unit"
            :absoluteDigits="1"
            :relativeDigits="0"
          />
        </td>
        <td>
          <MaintenanceTableDropdown
            :maintenance-object="maintenance_object"
            @doneButtonClicked="doneButtonClicked"
          />
        </td>
        <td>
          {{ maintenance_object.interval_amount }} {{ maintenance_object.interval_unit }}
        </td>
        <td v-if="!Object.keys(maintenance_object).includes('operating_hours')" />
        <td v-else>
          {{ maintenance_object.datetime_display | formatDateTime }}
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import { flattenNestedObjects } from '../../components/utils/DataProcessingUtils';
import MaintenanceTableDropdown from './MaintenanceTableDropdown.vue';
import LinearProgressMaintenanceInterval from '../../components/common/LinearProgressMaintenanceInterval.vue';

export default {
  name: 'MaintenanceTable',
  components: {
    MaintenanceTableDropdown,
    LinearProgressMaintenanceInterval,
  },
  props: {
    maintenanceEntries: {
      type: Object,
      required: true,
    },
  },
  created() {
  },
  updated() {
  },
  methods: {
    sort_maintenance(nestedEntries) {
      const flattenedEntries = flattenNestedObjects(nestedEntries);
      const filteredEntries = flattenedEntries
        .filter((i) => i.interval_type === 'planned cycle' || i.interval_type === 'estimated wear')
        .filter((i) => i.interval_unit !== 't');
      return this._.orderBy(filteredEntries, ['interval_unit', 'interval_amount'], ['desc', 'asc']);
    },
    doneButtonClicked(mtnId, selectedChips) {
      this.$emit('doneButtonClicked', mtnId, selectedChips);
    },
  },
};
</script>

<style scoped>

</style>
