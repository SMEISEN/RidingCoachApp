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
    /**
     * Dynamically defines the color of the setup avatars, showing the current click, depending on
     * the position of the click between the minimum, maximum and baseline click. If the current
     * click is smaller than the baseline, the color gradient is grey to blue, if greater, the color
     * gradient is grey to red.
     * @param {number} value current click
     * @param {number} minimum minimum click
     * @param {number} maximum maximal available clicks
     * @param {number} baseline the default number of clicks
     * @returns {string} rgb string for the given value
     */
    getColor(value, minimum, maximum, baseline) {
      const diff = value - baseline;
      if (diff < 0) {
        return this.linearGradient('#0D47A1', '#B3B5C6', value, minimum, baseline);
      }
      return this.linearGradient('#B3B5C6', '#B71C1C', value, baseline, maximum);
    },
    /**
     * Returns the rgb string corresponding to the given value and depending on the minimum and
     * maximum value, as well as given start and end color hex strings.
     * @param {string} startColour hex string of start color
     * @param {string} endColour hex string of end color
     * @param {number} value the value for which the color string is requested
     * @param {number} minimum minimum value, corresponding to the start color
     * @param {number} maximum maximum value, corresponding to the end color
     * @returns {string} rgb string for the given value
     */
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
    /**
     * Converts a linear scale (source) to a transformed linear scale (target) and returns the value
     * for the transformed linear scale.
     * @param {number} value the value for which the fade should be calculated
     * @param {number} fromSource the minimum value of the source scale
     * @param {number} toSource the maximum value of the source scale
     * @param {number} fromTarget the minimum value of the target scale
     * @param {number} toTarget the maximum value of the target scale
     * @returns {number} the percentage of color fade
     */
    mapColor(value, fromSource, toSource, fromTarget, toTarget) {
      return fromTarget
        + (
          ((value - fromSource) / (toSource - fromSource + Number.EPSILON)
          ) * (toTarget - fromTarget));
    },
    /**
     * Transforms a hex color string to object containing the numbers of the corresponding rgb-code.
     * @param {string} hex hex string of the color
     * @returns {{r: number, b: number, g: number}|null} rgb-object or null
     */
    hexToRgb(hex) {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      } : null;
    },
    /**
     * Filters the tire setups of a training item.
     * @param {number} index the number of the setup of a training.
     * @returns {array} array of tire setups or empty array
     */
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
    /**
     * Filters the suspension setups of a training item.
     * @param {number} index the number of the setup of a training.
     * @returns {array} array of suspension setups or empty array
     */
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
    /**
     * Filters the geometry setups of a training item.
     * @param {number} index the number of the setup of a training.
     * @returns {array} array of geometry setups or empty array
     */
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
    /**
     * Filters the engine setups of a training item.
     * @param {number} index the number of the setup of a training.
     * @returns {array} array of engine setups or empty array
     */
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
    /**
     * Filters valid lap times and assigns them to the corresponding track layouts
     * @param {number} index the number of the setup of a training.
     * @returns {array} array of lap time objects, e.g.,
     * [
     *  {
     *    track_layout: "A",
     *    laptimes: [44.59, 43.96, ...]
     *  },
     * {
     *    track_layout: "B",
     *    laptimes: [53.67, 52.84, ...]
     *  }
     * ]
     * or empty array
     */
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
    /**
     * Calculates the arithmetic mean of the given array of lap times.
     * @param {array} laptimes array of lap time numbers
     * @returns {number} arithmetic mean
     */
    average_laptime(laptimes) {
      return mean(laptimes).toFixed(2);
    },
    /**
     * Searches for the minimal value of the given array of lap times.
     * @param {array} laptimes array of lap time numbers
     * @returns {number} minimum value
     */
    min_laptime(laptimes) {
      return min(laptimes).toFixed(2);
    },
    /**
     * Calculates the standard deviation of the given array of lap times.
     * @param {array} laptimes array of lap time numbers
     * @returns {number} standard deviation
     */
    std_laptime(laptimes) {
      return std(laptimes).toFixed(2);
    },
  },
};
</script>

<style scoped>

</style>
