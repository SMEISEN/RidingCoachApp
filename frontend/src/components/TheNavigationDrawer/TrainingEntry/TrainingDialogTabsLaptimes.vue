<template>
  <v-simple-table
    light
    dense
  >
    <thead>
      <tr>
        <th
          class="text-left"
          style="width: 24px"
        >
          Lap
        </th>
        <th
          class="text-left"
          style="width: 24px"
        >
          Full
        </th>
        <th
          class="text-left"
          style="width: 24px"
        >
          Delta
        </th>
        <th
          v-if="Object.keys(sessionObject.laptimes[0].sectors).length >= 1"
          class="text-left"
          style="width: 24px"
        >
          Sector 1
        </th>
        <th
          v-if="Object.keys(sessionObject.laptimes[0].sectors).length >= 2"
          class="text-left"
          style="width: 24px"
        >
          Sector 2
        </th>
        <th
          v-if="Object.keys(sessionObject.laptimes[0].sectors).length >= 3"
          class="text-left"
          style="width: 24px"
        >
          Sector 3
        </th>
        <th
          v-if="Object.keys(sessionObject.laptimes[0].sectors).length >= 4"
          class="text-left"
          style="width: 24px"
        >
          Sector 4
        </th>
        <th
          v-if="Object.keys(sessionObject.laptimes[0].sectors).length >= 5"
          class="text-left"
          style="width: 24px"
        >
          Sector 5
        </th>
        <th
          class="text-left pl-8"
          style="width: 115px"
        >
          Valid
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(laptime_item) in laptimes"
        :key="'laptime/' + laptime_item.lap_id"
      >
        <td style="font-size: 12px">
          {{ laptime_item.lap_no }}
        </td>
        <td style="font-size: 12px">
          {{ laptime_item.laptime_seconds }}
        </td>
        <td style="font-size: 12px">
          {{ calculate_delta(laptime_item.laptime_seconds) }}
        </td>
        <td
          v-if="Object.keys(laptime_item.sectors).length >= 1"
          style="font-size: 12px"
        >
          {{ laptime_item.sectors['Sector 1'] }}
        </td>
        <td
          v-if="Object.keys(laptime_item.sectors).length >= 2"
          style="font-size: 12px"
        >
          {{ laptime_item.sectors['Sector 2'] }}
        </td>
        <td
          v-if="Object.keys(laptime_item.sectors).length >= 3"
          style="font-size: 12px"
        >
          {{ laptime_item.sectors['Sector 3'] }}
        </td>
        <td
          v-if="Object.keys(laptime_item.sectors).length >= 4"
          style="font-size: 12px"
        >
          {{ laptime_item.sectors['Sector 4'] }}
        </td>
        <td
          v-if="Object.keys(laptime_item.sectors).length >= 5"
          style="font-size: 12px"
        >
          {{ laptime_item.sectors['Sector 5'] }}
        </td>
        <td style="font-size: 12px">
          <v-btn
            :color="laptime_item.valid === true ? 'success' : 'error'"
            text
            @click.prevent="
              changeLapValidity(laptime_item.lap_id, laptime_item.valid);
              laptime_item.valid === true ? laptime_item.valid = false : laptime_item.valid = true"
          >
            {{ laptime_item.valid }}
          </v-btn>
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import { apiPutLaptimeItem } from '../../api/LaptimeApi';

export default {
  name: 'TrainingDialogTabsLaptimes',
  props: {
    sessionObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    session_index: 0,
  }),
  computed: {
    laptimes() {
      return this.sessionObject.laptimes;
    },
    fastest_lap() {
      return this.laptimes.reduce(
        (min, p) => (p.laptime_seconds < min ? p.laptime_seconds : min),
        this.laptimes[0].laptime_seconds,
      );
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    calculate_delta(thisLap) {
      return (thisLap - this.fastest_lap).toFixed(2);
    },
    changeLapValidity(lapId, valid) {
      const payload = { valid: !valid };
      apiPutLaptimeItem(payload, lapId);
    },
  },
};
</script>

<style scoped>

</style>
