<template>
  <v-simple-table
    v-if="Object.keys(trainingItem).includes('setups')"
    light
    dense
  >
    <thead>
      <tr>
        <th
          v-if="trainingItem.setups.length > 0"
          class="text-left"
          style="width: 24px"
        >
          Setup
        </th>
        <th
          v-if="tire_setups(0).length > 0"
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
        <th
          v-if="valid_laptimes(0).length > 0"
          class="text-left"
        >
          Laptimes
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
                <span class="white--text">
                  {{ index + 1 }}
                </span>
              </v-avatar>
            </template>
            <span>
              {{ setup_item.datetime_display | formatTime }}
            </span>
            <span v-if="setup_item.comment !== null">
              {{ ' - ' + setup_item.comment }}
            </span>
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
                  $store.getters.getCurrentBikeSlickFrontPressure - 0.5,
                  $store.getters.getCurrentBikeSlickFrontPressure + 0.5,
                  $store.getters.getCurrentBikeSlickFrontPressure + 0.0)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">
                  {{ setup_item.slick_pressure_front }}
                </span>
              </v-avatar>
            </template>
            <span>
              {{ 'Pressure of front slick tire' }}
            </span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.slick_pressure_rear !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.slick_pressure_rear + 0.0,
                  $store.getters.getCurrentBikeSlickRearPressure - 0.5,
                  $store.getters.getCurrentBikeSlickRearPressure + 0.5,
                  $store.getters.getCurrentBikeSlickRearPressure + 0.0)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">{{ setup_item.slick_pressure_rear }}</span>
              </v-avatar>
            </template>
            <span>
              {{ 'Pressure of rear slick tire' }}
            </span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.rain_pressure_front !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.rain_pressure_front + 0.0,
                  $store.getters.getCurrentBikeRainFrontPressure - 0.5,
                  $store.getters.getCurrentBikeRainFrontPressure + 0.5,
                  $store.getters.getCurrentBikeRainFrontPressure + 0.0)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">
                  {{ setup_item.rain_pressure_front }}
                </span>
              </v-avatar>
            </template>
            <span>
              {{ 'Pressure of front rain tire' }}
            </span>
          </v-tooltip>
          <v-tooltip
            v-if="setup_item.rain_pressure_rear !== null"
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-avatar
                :color="getColor(
                  setup_item.rain_pressure_rear + 0.0,
                  $store.getters.getCurrentBikeRainRearPressure - 0.5,
                  $store.getters.getCurrentBikeRainRearPressure + 0.5,
                  $store.getters.getCurrentBikeRainRearPressure + 0.0)"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">
                  {{ setup_item.rain_pressure_rear }}
                </span>
              </v-avatar>
            </template>
            <span>
              {{ 'Pressure of rear rain tire' }}
            </span>
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
                    suspension_setup.ticks_current + 0,
                    0,
                    suspension_setup.ticks_available + 0,
                    suspension_setup.ticks_standard + 0)"
                  size="24"
                  v-bind="attrs"
                  v-on="on"
                >
                  <span class="white--text">
                    {{ suspension_setup.ticks_current }}
                  </span>
                </v-avatar>
              </template>
              <span>
                {{ `${suspension_setup.group === null ? '' : suspension_setup.group}` }}
                {{ ` ${suspension_setup.name === null ? '' : suspension_setup.name}` }}
              </span>
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
                color="info"
                size="24"
                v-bind="attrs"
                v-on="on"
              >
                <span class="white--text">
                  {{ setup_item.operating_hours }}
                </span>
              </v-avatar>
            </template>
            <span>
              {{ 'Engine operating hours' }}
            </span>
          </v-tooltip>
          <span
            v-for="(engine_setup) in engine_setups(index)"
            :key="'setup/engine/' + engine_setup.group + '/' + engine_setup.name"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-avatar
                  :color="getColor(
                    engine_setup.ticks_current + 0,
                    0,
                    engine_setup.ticks_available + 0,
                    engine_setup.ticks_standard + 0)"
                  size="24"
                  v-bind="attrs"
                  v-on="on"
                >
                  <span class="white--text">
                    {{ engine_setup.ticks_current }}
                  </span>
                </v-avatar>
              </template>
              <span>
                {{ `${engine_setup.group === null ? '' : engine_setup.group}` }}
                {{ ` ${engine_setup.name === null ? '' : engine_setup.name}` }}
              </span>
            </v-tooltip>
          </span>
        </td>
        <td
          v-if="valid_laptimes(0).length > 0"
          style="font-size: 12px"
        >
          <div
            v-for="(object) in valid_laptimes(index)"
            :key="'setup/laptimes/' + object.track_layout"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip
                  color="info"
                  text-color="white"
                  small
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon
                    class="pr-1 ml-n1"
                    small
                  >
                    mdi-diameter-variant
                  </v-icon>
                  <span class="white--text">
                    {{
                      `${average_laptime(object.laptimes)}` }}
                  </span>
                </v-chip>
              </template>
              <span>
                {{ `Average laptime on layout "${object.track_layout}"` }}
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip
                  color="secondary darken-1"
                  text-color="white"
                  small
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon
                    class="pr-1 ml-n1"
                    small
                  >
                    mdi-sigma-lower
                  </v-icon>
                  <span class="white--text">
                    {{ `${std_laptime(object.laptimes)}` }}
                  </span>
                </v-chip>
              </template>
              <span>
                {{ `Standard deviation of lap times on layout "${object.track_layout}"` }}
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip
                  color="error darken-1"
                  text-color="white"
                  small
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon
                    class="pr-1 ml-n1"
                    small
                  >
                    mdi-fire
                  </v-icon>
                  <span class="white--text">
                    {{ `${min_laptime(object.laptimes)}` }}
                  </span>
                </v-chip>
              </template>
              <span>
                {{ `Fastet laptime on layout "${object.track_layout}"` }}
              </span>
            </v-tooltip>
          </div>
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
import {
  min,
  mean,
  std,
} from 'mathjs';

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
    getColor(value, minimum, maximum, baseline) {
      const diff = value - baseline;
      if (diff < 0) {
        return this.linearGradient('#0D47A1', '#B3B5C6', value, minimum, baseline);
      }
      return this.linearGradient('#B3B5C6', '#B71C1C', value, baseline, maximum);
    },
    linearGradient(startColour, endColour, value, minimum, maximum) {
      const startRGB = this.hexToRgb(startColour);
      const endRGB = this.hexToRgb(endColour);
      const percentFade = this.mapColor(value, minimum, maximum, 0, 1);
      let diffRed = endRGB.r - startRGB.r;
      let diffGreen = endRGB.g - startRGB.g;
      let diffBlue = endRGB.b - startRGB.b;
      diffRed = (diffRed * percentFade) + startRGB.r;
      diffGreen = (diffGreen * percentFade) + startRGB.g;
      diffBlue = (diffBlue * percentFade) + startRGB.b;
      return `rgb(${Math.round(diffRed)}, ${Math.round(diffGreen)}, ${Math.round(diffBlue)})`;
    },
    mapColor(value, fromSource, toSource, fromTarget, toTarget) {
      return fromTarget
        + (
          ((value - fromSource) / (toSource - fromSource + Number.EPSILON)
          ) * (toTarget - fromTarget));
    },
    hexToRgb(hex) {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      } : null;
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
    valid_laptimes(index) {
      if (Object.keys(this.trainingItem).includes('setups')) {
        if (this.trainingItem.setups.length > 0) {
          if (this.trainingItem.setups[index].sessions.length > 0) {
            const trackLayouts = {};
            for (let i = 0; i < this.trainingItem.setups[index].sessions.length; i += 1) {
              const layoutNames = this._.uniq(
                this._.map(
                  this.trainingItem.setups[index].sessions[i].laptimes, 'track_layout',
                ),
              ).sort();
              for (let j = 0; j < layoutNames.length; j += 1) {
                const layoutName = layoutNames[j];
                const validLaptimes = this.trainingItem.setups[index].sessions[i]
                  .laptimes.filter((o) => o.valid === true && o.track_layout === layoutName);
                if (validLaptimes.length > 0) {
                  const laptimeSeconds = validLaptimes.map((a) => a.laptime_seconds);
                  if (Object.keys(trackLayouts).includes(layoutName)) {
                    trackLayouts[layoutName] = [...trackLayouts[layoutName], ...laptimeSeconds];
                  } else {
                    trackLayouts[layoutName] = laptimeSeconds;
                  }
                }
              }
            }
            const result = [];
            for (let i = 0; i < Object.keys(trackLayouts).length; i += 1) {
              result.push({
                track_layout: Object.keys(trackLayouts)[i],
                laptimes: Object.values(trackLayouts)[i],
              });
            }
            return result;
          }
        }
      }
      return [];
    },
    average_laptime(laptimes) {
      return mean(laptimes).toFixed(2);
    },
    min_laptime(laptimes) {
      return min(laptimes).toFixed(2);
    },
    std_laptime(laptimes) {
      return std(laptimes).toFixed(2);
    },
  },
};
</script>

<style scoped>

</style>
