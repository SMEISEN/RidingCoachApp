/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  all_bikes: null,
  current_bike_id: null,
  current_bike_manufacturer: null,
  current_bike_model: null,
  current_bike_operating_hours: null,
  current_bike_year: null,
  current_bike_slick_front_pressure: null,
  current_bike_slick_rear_pressure: null,
  current_bike_rain_front_pressure: null,
  current_bike_rain_rear_pressure: null,
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
  getCurrentBikeSlickFrontPressure: (state) => state.current_bike_slick_front_pressure,
  getCurrentBikeSlickRearPressure: (state) => state.current_bike_slick_rear_pressure,
  getCurrentBikeRainFrontPressure: (state) => state.current_bike_rain_front_pressure,
  getCurrentBikeRainRearPressure: (state) => state.current_bike_rain_rear_pressure,
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
    state.current_bike_slick_front_pressure = selectedBike.slick_front_pressure;
    state.current_bike_slick_rear_pressure = selectedBike.slick_rear_pressure;
    state.current_bike_rain_front_pressure = selectedBike.rain_front_pressure;
    state.current_bike_rain_rear_pressure = selectedBike.rain_rear_pressure;
    state.current_bike_setup = selectedBike.setup;
  },
  updateCurrentBike(state, selectedBike) {
    state.current_bike_id = selectedBike.bike_id;
    state.current_bike_manufacturer = selectedBike.manufacturer;
    state.current_bike_model = selectedBike.model;
    state.current_bike_operating_hours = selectedBike.operating_hours;
    state.current_bike_year = selectedBike.year;
    state.current_bike_slick_front_pressure = selectedBike.slick_front_pressure;
    state.current_bike_slick_rear_pressure = selectedBike.slick_rear_pressure;
    state.current_bike_rain_front_pressure = selectedBike.rain_front_pressure;
    state.current_bike_rain_rear_pressure = selectedBike.rain_rear_pressure;
    state.current_bike_setup = selectedBike.setup;
  },
  setCurrentBikeId: (state, bikeId) => {
    state.current_bike_id = bikeId;
  },
  setCurrentBikeManufacturer: (state, bikeManufacturer) => {
    state.current_bike_manufacturer = bikeManufacturer;
  },
  setCurrentBikeModel: (state, bikeModel) => {
    state.current_bike_model = bikeModel;
  },
  setCurrentOperatingHours(state, operatingHours) {
    state.current_bike_operating_hours = operatingHours;
  },
  setCurrentBikeYear: (state, bikeYear) => {
    state.current_bike_year = bikeYear;
  },
  setCurrentBikeSlickFrontPressure: (state, slickFrontPressure) => {
    state.current_bike_slick_front_pressure = slickFrontPressure;
  },
  setCurrentBikeSlickRearPressure: (state, slickRearPressure) => {
    state.current_bike_slick_rear_pressure = slickRearPressure;
  },
  setCurrentBikeRainFrontPressure: (state, rainFrontPressure) => {
    state.current_bike_rain_front_pressure = rainFrontPressure;
  },
  setCurrentBikeRainRearPressure: (state, rainRearPressure) => {
    state.current_bike_rain_rear_pressure = rainRearPressure;
  },
  setCurrentBikeSetup: (state, bikeSetup) => {
    state.current_bike_setup = bikeSetup;
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
