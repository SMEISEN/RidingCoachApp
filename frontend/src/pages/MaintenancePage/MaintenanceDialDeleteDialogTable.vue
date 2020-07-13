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
          style="width: 145px"
        >
          Interval type
        </th>
        <th
          class="text-left"
          style="width: 45px"
        >
          Interval amount
        </th>
        <th
          class="text-left"
          style="width: 45px"
        >
          Interval type
        </th>
        <th
          class="text-left"
          style="width: 145px"
        >
          last modified
        </th>
        <th
          class="text-left"
          style="width: 145px"
        >
          created
        </th>
        <th
          class="text-left"
          style="width: 45px"
        >
          delete?
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
        <td>
          {{ maintenance_object.interval_type }}
        </td>
        <td>
          {{ maintenance_object.interval_amount }}
        </td>
        <td>
          {{ maintenance_object.interval_unit }}
        </td>
        <td>
          {{ maintenance_object.datetime_last_modified | formatDateTime }}
        </td>
        <td>
          {{ maintenance_object.datetime_created | formatDateTime }}
        </td>
        <td>
          <v-checkbox v-model="deleteCheckbox[maintenance_object.name]" />
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import { flattenNestedObjects } from '../../components/utils/DataProcessingUtils';

export default {
  name: 'MaintenanceDialDeleteDialogTable',
  props: {
    maintenanceEntries: {
      type: Object,
      required: true,
    },
    deleteCheckbox: {
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
  },
};
</script>

<style scoped>

</style>
