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
              @long-press-start="longPress(
                laptime_item.lap_id, lapIndex, laptime_item.track_layout)"
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
      <v-form v-model="valid">
        <v-card>
          <v-card-title class="headline">
            Add new layout name
          </v-card-title>
          <v-card-text class="pb-0">
            <v-text-field
              v-model="new_layout"
              :rules="name_rules"
              label="Track layout"
              required
            />
          </v-card-text>
          <v-card-actions class="py-0 my-n3 pr-5">
            <v-spacer />
            <v-switch
              v-model="apply_to_all"
              label="apply to all"
            />
          </v-card-actions>
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="secondary"
              text
              @click="closeDialog()"
            >
              Close
            </v-btn>
            <v-btn
              color="secondary"
              text
              :disabled="!valid"
              @click="saveLayout()"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
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
    lap_index: null,
    valid: false,
    apply_to_all: false,
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
    name_rules() {
      return [
        (v) => !!v || 'Please define a name',
        (v) => !this.track_layouts.includes(v) || 'Name does already exist',
      ];
    },
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
      if (this.track_layouts.length > 1) {
        const currentIndex = this.track_layouts.indexOf(trackLayout);
        const nextLayout = (currentIndex === this.track_layouts.length - 1)
          ? (this.track_layouts[0]) : (this.track_layouts[currentIndex + 1]);
        this.laptimes[lapIndex].track_layout = nextLayout;
        const payload = { track_layout: nextLayout };
        this.putLaptimeItem(payload, lapId);
      }
      this.closeDialog();
    },
    longPress(lapId, lapIndex, trackLayout) {
      this.old_layout = trackLayout;
      this.new_layout = String.fromCharCode(
        this.track_layouts[this.track_layouts.length - 1].charCodeAt(0) + 1,
      );
      this.lap_id = lapId;
      this.lap_index = lapIndex;
      this.layout_dialog = true;
    },
    saveLayout() {
      const lapId = this.lap_id;
      if (this.apply_to_all === true) {
        for (let i = 0; i < this.laptimes.length; i += 1) {
          if (this.laptimes[i].track_layout === this.old_layout) {
            const payload = { track_layout: this.new_layout };
            this.laptimes[i].track_layout = this.new_layout;
            this.putLaptimeItem(payload, lapId);
          }
        }
      } else {
        const payload = { track_layout: this.new_layout };
        this.laptimes[this.lap_index].track_layout = this.new_layout;
        this.putLaptimeItem(payload, lapId);
      }
      this.closeDialog();
    },
    closeDialog() {
      this.new_layout = '';
      this.lap_id = null;
      this.layout_dialog = false;
    },
    putLaptimeItem(payload, lapId) {
      apiPutLaptimeItem(payload, lapId)
        .then(() => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'New track layout defined',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>
