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
          Setup
        </th>
        <th
          v-if="tire_setups(0)"
          class="text-left"
        >
          Tires
        </th>
        <th
          v-if="suspension_setups(0).length > 0"
          class="text-left"
        >
          Suspension
        </th>
        <th
          v-if="geometry_setups(0).length > 0"
          class="text-left"
        >
          Geometry
        </th>
        <th
          v-if="trainingItem.setups.filter((i) => i.operating_hours !== null).length > 0"
          class="text-left"
        >
          Engine
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(setup_item, index) in trainingItem.setups"
        :key="'setup/' + setup_item.setup_id"
      >
        <td style="font-size: 12px">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                color="primary"
                tile
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ index + 1 }}</span>
              </v-avatar>
            </template>
            <span>{{ setup_item.datetime_display | formatTime }}</span>
            <span v-if="setup_item.comment !== null">{{ ' - ' + setup_item.comment }}</span>
          </v-tooltip>
        </td>
        <td
          v-if="tire_setups(0)"
          style="font-size: 12px"
        >
          <v-tooltip
            v-if="setup_item.slick_pressure_front !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.slick_pressure_front + 0.0,
                  $store.getters.getCurrentBikeSlickFrontPressure + 0.0,
                  $store.getters.getCurrentBikeSlickFrontPressure + 0.3)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.slick_pressure_front }}</span>
              </v-avatar>
            </template>
            <span>{{ 'Pressure of front slick tire' }}</span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.slick_pressure_rear !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.slick_pressure_rear + 0.0,
                  $store.getters.getCurrentBikeSlickRearPressure + 0.0,
                  $store.getters.getCurrentBikeSlickRearPressure + 0.3)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.slick_pressure_rear }}</span>
              </v-avatar>
            </template>
            <span>{{ 'Pressure of rear slick tire' }}</span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.rain_pressure_front !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.rain_pressure_front + 0.0,
                  $store.getters.getCurrentBikeRainFrontPressure + 0.0,
                  $store.getters.getCurrentBikeRainFrontPressure + 0.3)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.rain_pressure_front }}</span>
              </v-avatar>
            </template>
            <span>{{ 'Pressure of front rain tire' }}</span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.rain_pressure_rear !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.rain_pressure_rear + 0.0,
                  $store.getters.getCurrentBikeRainRearPressure + 0.0,
                  $store.getters.getCurrentBikeRainRearPressure + 0.3)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.rain_pressure_rear }}</span>
              </v-avatar>
            </template>
            <span>{{ 'Pressure of rear rain tire' }}</span>
          </v-tooltip>
        </td>
        <td
          v-if="suspension_setups(0).length > 0"
          style="font-size: 12px"
        >
          <span
            v-for="(suspension_setup) in suspension_setups(index)"
            :key="'setup/suspension/' + suspension_setup.group + '/' + suspension_setup.name"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-avatar
                  :color="getColor(
                    suspension_setup.ticks_current,
                    suspension_setup.ticks_standard,
                    suspension_setup.ticks_available)"
                  size="24"
                  v-bind="attrs"
                  v-on="on"
                >
                  <span class="white--text">{{ suspension_setup.ticks_current }}</span>
                </v-avatar>
              </template>
              <span>{{ `${suspension_setup.group} ${suspension_setup.name}` }}</span>
            </v-tooltip>
          </span>
        </td>
        <td
          v-if="geometry_setups(0).length > 0"
          style="font-size: 12px"
        />
        <td
          v-if="setup_item.operating_hours !== null"
          style="font-size: 12px"
        >
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                color="primary"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.operating_hours }}</span>
              </v-avatar>
            </template>
            <span>{{ 'Engine operating hours' }}</span>
          </v-tooltip>
          <span
            v-for="(engine_setup) in engine_setups(index)"
            :key="'setup/engine/' + engine_setup.group + '/' + engine_setup.name"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-avatar
                  :color="getColor(
                    engine_setup.ticks_current,
                    engine_setup.ticks_standard,
                    engine_setup.ticks_available)"
                  size="24"
                  v-bind="attrs"
                  v-on="on"
                >
                  <span class="white--text">{{ engine_setup.ticks_current }}</span>
                </v-avatar>
              </template>
              <span>{{ `${engine_setup.group} ${engine_setup.name}` }}</span>
            </v-tooltip>
          </span>
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
export default {
  name: 'TimelineCardTable',
  props: {
    trainingItem: {
      type: Object,
      required: true,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    getColor(current, baseline, available) {
      const diff = current - baseline;
      const max = available;
      const min = 0;
      if (diff < 0) {
        return `rgb(
          ${13 + ((max - current) / (baseline - min)) * 50},
          ${71 + ((max - current) / (baseline - min)) * 25},
          161`;
      } if (diff === 0) {
        return 'rgb(179, 181, 198)';
      }
      return `rgb(
          183,
          ${28 + ((current - min) / (max - baseline)) * 35},
          ${28 + ((current - min) / (max - baseline)) * 35}`;
    },
    tire_setups(index) {
      if (Object.keys(this.trainingItem).includes('setups')) {
        if (this.trainingItem.setups.length > 0) {
          if (this.trainingItem.setups[index].setup.length > 0) {
            return this.trainingItem.setups[index].setup
              .filter((i) => i.slick_pressure_front !== null
                || i.slick_pressure_rear !== null
                || i.rain_pressure_front !== null
                || i.rain_pressure_rear !== null);
          }
        }
      }
      return [];
    },
    suspension_setups(index) {
      if (Object.keys(this.trainingItem).includes('setups')) {
        if (this.trainingItem.setups.length > 0) {
          if (this.trainingItem.setups[index].setup.length > 0) {
            return this.trainingItem.setups[index].setup.filter((i) => i.category === 'Suspension');
          }
        }
      }
      return [];
    },
    geometry_setups(index) {
      if (Object.keys(this.trainingItem).includes('setups')) {
        if (this.trainingItem.setups.length > 0) {
          if (this.trainingItem.setups[index].setup.length > 0) {
            return this.trainingItem.setups[index].setup.filter((i) => i.category === 'Geometry');
          }
        }
      }
      return [];
    },
    engine_setups(index) {
      if (Object.keys(this.trainingItem).includes('setups')) {
        if (this.trainingItem.setups.length > 0) {
          if (this.trainingItem.setups[index].setup.length > 0) {
            return this.trainingItem.setups[index].setup.filter((i) => i.category === 'Engine');
          }
        }
      }
      return [];
    },
  },
};
</script>

<style scoped>

</style>
