/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  current_tire_front_id: null,
  current_tire_front_category: null,
  current_tire_front_pressure: null,
  current_tire_front_operating_hours: null,
  current_tire_rear_id: null,
  current_tire_rear_category: null,
  current_tire_rear_pressure: null,
  current_tire_rear_operating_hours: null,
  last_tire_updated_id: null,
});
const state = getDefaultState();
const getters = {
  getCurrentTireFrontId: (state) => state.current_tire_front_id,
  getCurrentTireFrontCategory: (state) => state.current_tire_front_category,
  getCurrentTireFrontPressure: (state) => state.current_tire_front_pressure,
  getCurrentTireFrontOperatingHours: (state) => state.current_tire_front_operating_hours,
  getCurrentTireRearId: (state) => state.current_tire_rear_id,
  getCurrentTireRearCategory: (state) => state.current_tire_rear_category,
  getCurrentTireRearPressure: (state) => state.current_tire_rear_pressure,
  getCurrentTireRearOperatingHours: (state) => state.current_tire_rear_operating_hours,
  getLastTireUpdated: (state) => state.last_tire_updated_id,
};
const mutations = {
  lastTireUpdatedId(state, updatedId) {
    state.last_tire_updated_id = updatedId;
  },
  selectFrontTire(state, selectedFrontId) {
    state.current_tire_front_id = selectedFrontId;
  },
  selectRearTire(state, selectedRearId) {
    state.current_tire_rear_id = selectedRearId;
  },
  updateCurrentFrontTire(state, selectedFront) {
    state.current_tire_front_id = selectedFront.tire_id;
    state.current_tire_front_category = selectedFront.category;
    state.current_tire_front_pressure = selectedFront.pressure;
    state.current_tire_front_operating_hours = selectedFront.operating_hours;
  },
  updateCurrentRearTire(state, selectedRear) {
    state.current_tire_rear_id = selectedRear.tire_id;
    state.current_tire_rear_category = selectedRear.category;
    state.current_tire_rear_pressure = selectedRear.pressure;
    state.current_tire_rear_operating_hours = selectedRear.operating_hours;
  },
  updateCurrentFrontTireOperatingHours(state, operatingHours) {
    state.current_tire_front_operating_hours = operatingHours;
  },
  updateCurrentRearTireOperatingHours(state, operatingHours) {
    state.current_tire_rear_operating_hours = operatingHours;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
