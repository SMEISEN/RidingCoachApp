<template>
  <v-simple-table
    hide-default-header
    hide-default-footer
    dense
  >
    <tbody>
    <tr v-for="(wear_object, index) in wear_object"
        v-bind:key="index + $store.getters.getCurrentBikeOperatingHours">
      <td>{{ wear_object.name }}</td>
      <td v-if="!Object.keys(wear_object).includes('operating_hours')"></td>
      <td v-else style="min-width: 120px;width: 120px;max-width: 120px">
        <LinearProgressIntervalHours
          :hours_latest="wear_object.operating_hours"
          :hours_interval="wear_object.interval_amount"
          :hours_current="$store.getters.getCurrentBikeOperatingHours"
        />
      </td>
    </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import LinearProgressIntervalHours from '../../components/common/LinearProgressIntervalHours';

export default {
  name: 'DashboardWearState',
  props: {
    wear_object: {
      type: Object,
      required: true,
    },
  },
  components: {
    LinearProgressIntervalHours,
  },
}
</script>

<style scoped>

</style>
