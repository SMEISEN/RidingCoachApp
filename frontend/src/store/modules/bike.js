/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const state = () => ({
  current_bike_id: null,
  current_bike_manufacturer: null,
  current_bike_model: null,
  current_bike_operating_hours: null,
  current_bike_year: null,
});
const getters = {
  getCurrentBikeId: (state) => state.current_bike_id,
  getCurrentBikeManufacturer: (state) => state.current_bike_manufacturer,
  getCurrentBikeModel: (state) => state.current_bike_model,
  getCurrentBikeOperatingHours: (state) => state.current_bike_operating_hours,
  getCurrentBikeYear: (state) => state.current_bike_year,
};
const mutations = {
  selectBike(state, selectedBike) {
    state.current_bike_id = selectedBike.bike_id;
    state.current_bike_manufacturer = selectedBike.manufacturer;
    state.current_bike_model = selectedBike.model;
    state.current_bike_operating_hours = selectedBike.operating_hours;
    state.current_bike_year = selectedBike.year;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};