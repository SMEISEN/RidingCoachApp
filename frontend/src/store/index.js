import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    current_bike_id: '',
    current_bike_manufacturer: '',
    current_bike_model: '',
    current_bike_operating_hours: '',
    current_bike_year: '',
  },
  getters: {
    getCurrentBikeId(state) {
      return state.current_bike_id;
    },
    getCurrentBikeManufacturer(state) {
      return state.current_bike_manufacturer;
    },
    getCurrentBikeModel(state) {
      return state.current_bike_model;
    },
    getCurrentBikeOperatingHours(state) {
      return state.current_bike_operating_hours;
    },
    getCurrentBikeYear(state) {
      return state.current_bike_year;
    },
  },
  mutations: {
    selectBike(state, selectedBike) {
      state.current_bike_id = selectedBike.bike_id;
      state.current_bike_manufacturer = selectedBike.manufacturer;
      state.current_bike_model = selectedBike.model;
      state.current_bike_operating_hours = selectedBike.operating_hours;
      state.current_bike_year = selectedBike.year;
    },
  },
  actions: {},
  plugins: [createPersistedState({
    storage: {
      getItem: (key) => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 90, secure: true }),
      removeItem: (key) => Cookies.remove(key),
    },
  })],
});
