/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  all_bikes: null,
  current_bike_id: null,
  current_bike_manufacturer: null,
  current_bike_model: null,
  current_bike_operating_hours: null,
  current_bike_year: null,
  current_bike_setup: null,
});
const state = getDefaultState();
const getters = {
  getAllBikes: (state) => state.all_bikes,
  getCurrentBikeId: (state) => state.current_bike_id,
  getCurrentBikeManufacturer: (state) => state.current_bike_manufacturer,
  getCurrentBikeModel: (state) => state.current_bike_model,
  getCurrentBikeOperatingHours: (state) => state.current_bike_operating_hours,
  getCurrentBikeYear: (state) => state.current_bike_year,
  getCurrentBikeSetup: (state) => state.current_bike_setup,
};
const mutations = {
  setAllBikes(state, bikes) {
    state.all_bikes = bikes;
  },
  selectBike(state, selectedBike) {
    state.current_bike_id = selectedBike.bike_id;
    state.current_bike_manufacturer = selectedBike.manufacturer;
    state.current_bike_model = selectedBike.model;
    state.current_bike_operating_hours = selectedBike.operating_hours;
    state.current_bike_year = selectedBike.year;
    state.current_bike_setup = selectedBike.setup;
  },
  setOperatingHours(state, operatingHours) {
    state.current_bike_operating_hours = operatingHours;
  },
  resetBikeState(state) {
    Object.assign(state, getDefaultState());
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
