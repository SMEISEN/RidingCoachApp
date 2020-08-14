<template>
  <v-row
    no-gutters
    justify="center"
  >
    <v-tooltip
      v-for="(weather_item, index) in weatherDaily"
      :key="'weather/' + index"
      bottom
    >
      <template v-slot:activator="{ on, attrs }">
        <v-avatar
          size="20"
          v-bind="attrs"
          v-on="on"
        >
          <v-icon
            v-if="weather_item.weather_code === 'clear'"
            small
          >
            mdi-weather-sunny
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'mostly_clear'"
            small
          >
            mdi-weather-partly-cloudy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'partly_cloudy'"
            small
          >
            mdi-weather-partly-cloudy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'mostly_cloudy'"
            small
          >
            mdi-weather-cloudy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'cloudy'"
            small
          >
            mdi-weather-cloudy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'fog'"
            small
          >
            mdi-weather-fog
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'fog_light'"
            small
          >
            mdi-weather-fog
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'tstorm'"
            small
          >
            mdi-weather-lightning-rainy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'flurries'"
            small
          >
            mdi-weather-windy-variant
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'snow_light'"
            small
          >
            mdi-weather-snowy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'snow'"
            small
          >
            mdi-weather-snowy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'snow_light'"
            small
          >
            mdi-weather-snowy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'snow_heavy'"
            small
          >
            mdi-weather-snowy-heavy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'ice_pellets_light'"
            small
          >
            mdi-weather-hail
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'ice_pellets'"
            small
          >
            mdi-weather-hail
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'ice_pellets_heavy'"
            small
          >
            mdi-weather-hail
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'drizzle'"
            small
          >
            mdi-weather-pouring
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'freezing_drizzle'"
            small
          >
            mdi-weather-snowy-rainy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'freezing_rain_light'"
            small
          >
            mdi-weather-snowy-rainy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'freezing_rain'"
            small
          >
            mdi-weather-snowy-rainy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'freezing_rain_heavy'"
            small
          >
            mdi-weather-snowy-rainy
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'rain_light'"
            small
          >
            mdi-weather-pouring
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'rain'"
            small
          >
            mdi-weather-pouring
          </v-icon>
          <v-icon
            v-if="weather_item.weather_code === 'rain_heavy'"
            small
          >
            mdi-weather-pouring
          </v-icon>
        </v-avatar>
      </template>
      <span>{{ `${Math.round(weather_item.temp, 0)} °C` }}</span>
    </v-tooltip>
  </v-row>
</template>

<script>
export default {
  name: 'TimelineCardTitleWeather',
  props: {
    weatherDaily: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
