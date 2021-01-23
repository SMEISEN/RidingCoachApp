<template>
  <div>
    <v-simple-table
      v-if="laptimes.length > 0"
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
            v-if="Object.keys(laptimes[0].sectors).length >= 1"
            class="text-left"
            style="width: 24px"
          >
            Sector 1
          </th>
          <th
            v-if="Object.keys(laptimes[0].sectors).length >= 2"
            class="text-left"
            style="width: 24px"
          >
            Sector 2
          </th>
          <th
            v-if="Object.keys(laptimes[0].sectors).length >= 3"
            class="text-left"
            style="width: 24px"
          >
            Sector 3
          </th>
          <th
            v-if="Object.keys(laptimes[0].sectors).length >= 4"
            class="text-left"
            style="width: 24px"
          >
            Sector 4
          </th>
          <th
            v-if="Object.keys(laptimes[0].sectors).length >= 5"
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
          <th
            class="text-left pl-11"
            style="width: 115px"
          >
            Layout
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(laptime_item, lapIndex) in laptimes"
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
              @click.prevent="changeLapValidity(
                laptime_item.lap_id, lapIndex, laptime_item.valid)"
            >
              {{ laptime_item.valid }}
            </v-btn>
          </td>
          <td style="font-size: 12px">
            <v-btn
              v-long-press="500"
              min-width="100"
              text
              @long-press-start="longPress(laptime_item.lap_id, laptime_item.track_layout)"
              @click.prevent="changeLapTrackLayout(
                laptime_item.lap_id, lapIndex, laptime_item.track_layout)"
            >
              {{ laptime_item.track_layout }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
    <v-dialog
      v-model="layout_dialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          Add new layout name
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="new_layout"
          >
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            text
            @click="closeClicked()"
          >
            Close
          </v-btn>

          <v-btn
            color="secondary"
            text
            @click="saveClicked()"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LongPress from 'vue-directive-long-press';
import { apiPutLaptimeItem } from '../../api/LaptimeApi';

export default {
  name: 'TrainingDialogTabsLaptimes',
  directives: {
    'long-press': LongPress,
  },
  props: {
    sessionObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    session_index: 0,
    layout_dialog: false,
    new_layout: '',
    lap_id: null,
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
    track_layouts() {
      return this._.uniq(this._.map(this.laptimes, 'track_layout')).sort();
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
    changeLapValidity(lapId, lapIndex, valid) {
      this.laptimes[lapIndex].valid = !valid;
      let payload = { valid: !valid };
      apiPutLaptimeItem(payload, lapId)
        .then(() => {
          payload = { state: true };
          if (valid === true) {
            payload.color = 'error';
            payload.message = 'Lap time set invalid';
          } else {
            payload.color = 'success';
            payload.message = 'Lap time set valid';
          }
          this.$store.commit('setInfoSnackbar', payload);
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    changeLapTrackLayout(lapId, lapIndex, trackLayout) {
      const currentIndex = this.track_layouts.indexOf(trackLayout);
      const nextIndex = (currentIndex === this.track_layouts.length - 1)
        ? (this.track_layouts[0]) : (this.track_layouts[currentIndex + 1]);
      this.laptimes[lapIndex].track_layout = nextIndex;
    },
    longPress(lapId, trackLayout) {
      this.new_layout = trackLayout;
      this.lap_id = lapId;
      this.layout_dialog = true;
    },
    closeClicked() {
      this.new_layout = '';
      this.lap_id = null;
      this.layout_dialog = false;
    },
    saveClicked() {
      this.new_layout = '';
      this.lap_id = null;
      this.layout_dialog = false;
    },
  },
};
</script>

<style scoped>

</style>
