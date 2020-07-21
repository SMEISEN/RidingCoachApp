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
          <LinearProgressIntervalYears
            :date-latest="maintenance_object.datetime_display"
          />
        </td>
        <td v-else>
          <LinearProgressIntervalHours
            :hours-latest="maintenance_object.operating_hours"
            :hours-interval="maintenance_object.interval_amount"
            :hours-current="$store.getters.getCurrentBikeOperatingHours"
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
import {
  flattenNestedObjects,
  processStateOfIntervalHours,
  processLeftIntervalHours,
  processStateOfIntervalYears,
  processLeftIntervalYears,
} from '../../components/utils/DataProcessingUtils';
import MaintenanceTableDropdown from './MaintenanceTableDropdown.vue';
import LinearProgressIntervalHours from '../../components/common/LinearProgressIntervalHours.vue';
import LinearProgressIntervalYears from '../../components/common/LinearProgressIntervalYears.vue';

export default {
  name: 'MaintenanceTable',
  components: {
    MaintenanceTableDropdown,
    LinearProgressIntervalHours,
    LinearProgressIntervalYears,
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
      return this._.orderBy(flattenedEntries, ['interval_unit', 'interval_amount'], ['desc', 'asc']);
    },
    currentStateIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      return processStateOfIntervalHours(HoursLatest, HoursInterval, BikeHours, 2);
    },
    leftIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      return processLeftIntervalHours(HoursLatest, HoursInterval, BikeHours, 2);
    },
    currentStateIntervalYears(DateLatest) {
      return processStateOfIntervalYears(DateLatest, 2);
    },
    leftIntervalYears(DateLatest) {
      return processLeftIntervalYears(DateLatest, 2);
    },
    doneButtonClicked(mtnId, selectedChips) {
      this.$emit('doneButtonClicked', mtnId, selectedChips);
    },
  },
};
</script>

<style scoped>

</style>
