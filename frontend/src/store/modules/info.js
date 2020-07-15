/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const state = () => ({
  snackbar_state: false,
  snackbar_color: null,
  snackbar_message: null,
});
const getters = {
  getInfoSnackbarState: (state) => state.snackbar_state,
  getInfoSnackbarColor: (state) => state.snackbar_color,
  getInfoSnackbarMessage: (state) => state.snackbar_message,
};
const mutations = {
  setInfoSnackbar(state, payload) {
    state.snackbar_state = payload.state;
    state.snackbar_color = payload.color;
    state.snackbar_message = payload.message;
  },
  setInfoSnackbarState(state, snackbarState) {
    state.snackbar_state = snackbarState;
  },
  setInfoSnackbarColor(state, snackbarColor) {
    state.snackbar_color = snackbarColor;
  },
  setInfoSnackbarMessage(state, snackbarMessage) {
    state.snackbar_message = snackbarMessage;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
