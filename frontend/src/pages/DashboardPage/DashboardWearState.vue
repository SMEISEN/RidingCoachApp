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
        <td v-if="!Object.keys(wearObject).includes('operating_hours')" />
        <td
          v-else
          style="min-width: 120px;width: 120px;max-width: 120px"
        >
          <LinearProgressIntervalHours
            :hours-latest="wear_object.operating_hours"
            :hours-interval="wear_object.interval_amount"
            :hours-current="$store.getters.getCurrentBikeOperatingHours"
          />
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import LinearProgressIntervalHours from '../../components/common/LinearProgressIntervalHours.vue';

export default {
  name: 'DashboardWearState',
  components: {
    LinearProgressIntervalHours,
  },
  props: {
    wearObject: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
