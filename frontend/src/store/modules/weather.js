/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  current_temperature_air_deg_c: null,
  current_temperature_track_deg_c: null,
});
const state = getDefaultState();
const getters = {
  getCurrentTemperatureAirDegC: (state) => state.current_temperature_air_deg_c,
  getCurrentTemperatureTrackDegC: (state) => state.current_temperature_track_deg_c,
};
const mutations = {
  setCurrentTemperatureAirDegC(state, temperatureAirDegC) {
    state.current_temperature_air_deg_c = temperatureAirDegC;
  },
  setCurrentTemperatureTrackDegC(state, temperatureAirDegC) {
    state.current_temperature_track_deg_c = temperatureAirDegC;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
