/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const state = () => ({
  navigation_drawer: false,
  bike_dialog: false,
  bike_edit_flag: false,
  training_dialog: false,
});
const getters = {
  getNavigationDrawerState: (state) => state.navigation_drawer,
  getBikeDialogState: (state) => state.bike_dialog,
  getBikeEditFlag: (state) => state.bike_edit_flag,
  getTrainingDialogState: (state) => state.training_dialog,
};
const mutations = {
  setNavigationDrawerState(state, drawerState) {
    state.navigation_drawer = drawerState;
  },
  setBikeDialogState(state, dialogState) {
    state.bike_dialog = dialogState;
  },
  setBikeEditFlag(state, editFlag) {
    state.bike_edit_flag = editFlag;
  },
  setTrainingDialogState(state, dialogState) {
    state.training_dialog = dialogState;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
