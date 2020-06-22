<template>
  <v-simple-table dense fixed-header height="300px">
    <thead>
    <tr>
      <th class="text-left" style="min-width: 120px">Name</th>
      <th class="text-left" style="min-width: 120px;width: 120px;max-width: 120px">State</th>
      <th class="button" style="min-width: 120px;width: 120px;max-width: 120px"></th>
      <th class="text-left" style="min-width: 80px;width: 80px;max-width: 80px">Interval</th>
      <th class="text-left" style="width: 145px">Date</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="maintenance_object in sort_maintenance(maintenance_entries)"
        v-bind:key="maintenance_object.maintenance_id">
      <td style="font-size: 12px">{{ maintenance_object.name }}</td>
      <td v-if="!Object.keys(maintenance_object).includes('operating_hours')"></td>
      <td v-else-if="maintenance_object.interval_unit === 'a'">
        <LinearProgressIntervalYears
          :date_latest="maintenance_object.datetime_display"
        />
      </td>
      <td v-else>
        <LinearProgressIntervalHours
          :hours_latest="maintenance_object.operating_hours"
          :hours_interval="maintenance_object.interval_amount"
          :hours_current="$store.getters.getCurrentBikeOperatingHours"
        />
      </td>
      <td>
        <v-btn color="success" text
               @click="doneButtonClicked(maintenance_object.maintenance_id)">
          Done!
        </v-btn>
      </td>
      <td>
        {{ maintenance_object.interval_amount }} {{ maintenance_object.interval_unit }}
      </td>
      <td v-if="!Object.keys(maintenance_object).includes('operating_hours')"> </td>
      <td v-else>
        {{ maintenance_object.datetime_display | formatDateTime }}
      </td>
    </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import {DataProcessingUtils} from '../../components/utils/DataProcessingUtils';
import _ from 'lodash';
import LinearProgressIntervalHours from '../../components/common/LinearProgressIntervalHours';
import LinearProgressIntervalYears from '../../components/common/LinearProgressIntervalYears';

export default {
  name: 'MaintenanceTable',
  props: {
    maintenance_entries: {
      type: Object,
      required: true,
    }
  },
  components: {
    LinearProgressIntervalHours,
    LinearProgressIntervalYears,
  },
  methods: {
    sort_maintenance(maintenance_entries) {
      maintenance_entries = DataProcessingUtils.flattenNestedObjects(maintenance_entries);
      return _.orderBy(maintenance_entries, ['interval_unit', 'interval_amount'], ['desc', 'asc']);
    },
    currentStateIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      return DataProcessingUtils
        .processStateOfIntervalHours(HoursLatest, HoursInterval, BikeHours, 2);
    },
    leftIntervalHours(HoursLatest, HoursInterval, BikeHours) {
      return DataProcessingUtils
        .processLeftIntervalHours(HoursLatest, HoursInterval, BikeHours, 2);
    },
    currentStateIntervalYears(DateLatest) {
      return DataProcessingUtils
        .processStateOfIntervalYears(DateLatest, 2);
    },
    leftIntervalYears(DateLatest) {
      return DataProcessingUtils
        .processLeftIntervalYears(DateLatest, 2);
    },
    doneButtonClicked(MtnId) {
      this.$emit('doneButtonClicked', MtnId);
    },
  }
}
</script>

<style scoped>

</style>
