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
        v-for="maintenance_object in maintenance_entries"
        :key="maintenance_object.maintenance_id"
      >
        <td style="font-size: 12px">
          {{ maintenance_object.name }}
        </td>
        <td v-if="!Object.keys(maintenance_object).includes('operating_hours')" />
        <td v-else-if="maintenance_object.interval_unit === 'a'">
          <LinearProgressMaintenanceInterval
            :interval-state="maintenance_object.interval_state"
            :interval-unit="'d'"
            :absolute-digitsto-precision="3"
            :relative-digits-to-fixed="0"
          />
        </td>
        <td v-else>
          <LinearProgressMaintenanceInterval
            :interval-state="maintenance_object.interval_state"
            :interval-unit="maintenance_object.interval_unit"
            :absolute-digitsto-precision="2"
            :relative-digits-to-fixed="0"
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
      type: Array,
      required: true,
    },
  },
  computed: {
    /**
     * Filters the nested object of maintenance items and flattens it to an array.
     * Retain the interval types "planned cycle" and "estimated wear" and remove items with the
     * interval unit "t".
     * @returns {array} array of maintenance items, e.g.
     * [
     *    {
     *      bike_id: "...",
     *      comment: "...",
     *      ...
     *      name: "...",
     *      ...
     *    },
     *    ...
     * ]
     */
    maintenance_entries() {
      const filteredEntries = this.maintenanceEntries
        .filter((i) => i.interval_type === 'planned cycle' || i.interval_type === 'estimated wear')
        .filter((i) => i.interval_unit !== 't');
      return this._.orderBy(filteredEntries,
        ['interval_unit', 'interval_amount'],
        ['desc', 'asc']);
    },
  },
  methods: {
    /**
     * Emits a message to the parent that the done button was clicked and parses the maintenance id
     * and the selected maintenance tags.
     * @param {string} mtnId maintenance id
     * @param {array} selectedChips array of selected maintenance tags
     */
    doneButtonClicked(mtnId, selectedChips) {
      this.$emit('doneButtonClicked', mtnId, selectedChips);
    },
  },
};
</script>
