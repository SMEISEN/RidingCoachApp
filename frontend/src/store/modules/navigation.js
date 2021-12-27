/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  navigation_drawer: false,
  bike_dialog: false,
  bike_edit_flag: false,
  training_edit_id: null,
  training_dialog: false,
  training_setup_panel: 0,
  training_setup_tabs: 1,
  training_setup_tab: 0,
  training_session_tabs: 1,
  training_session_tab: 0,
  training_session_panel: 0,
  tire_dialog: false,
});
const state = getDefaultState();
const getters = {
  getNavigationDrawerState: (state) => state.navigation_drawer,
  getBikeDialogState: (state) => state.bike_dialog,
  getBikeEditFlag: (state) => state.bike_edit_flag,
  getTrainingEditId: (state) => state.training_edit_id,
  getTrainingDialogState: (state) => state.training_dialog,
  getTrainingDialogSetupPanel: (state) => state.training_setup_panel,
  getTrainingDialogSetupTabs: (state) => state.training_setup_tabs,
  getTrainingDialogSetupActiveTab: (state) => state.training_setup_tab,
  getTrainingDialogSessionTabs: (state) => state.training_session_tabs,
  getTrainingDialogSessionActiveTab: (state) => state.training_session_tab,
  getTrainingDialogSessionPanel: (state) => state.training_session_panel,
  getTireDialogState: (state) => state.tire_dialog,
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
  setTrainingEditId(state, trainingId) {
    state.training_edit_id = trainingId;
  },
  setTrainingDialogState(state, dialogState) {
    state.training_dialog = dialogState;
  },
  setTrainingDialogSetupPanel(state, setupPanel) {
    state.training_setup_panel = setupPanel;
  },
  setTrainingDialogSetupTabs(state, setupTabs) {
    state.training_setup_tabs = setupTabs;
  },
  setTrainingDialogSetupActiveTab(state, activeTab) {
    state.training_setup_tab = activeTab;
  },
  setTrainingDialogSessionTabs(state, activeTab) {
    state.training_session_tabs = activeTab;
  },
  setTrainingDialogSessionActiveTab(state, activeTab) {
    state.training_session_tab = activeTab;
  },
  setTrainingDialogSessionPanel(state, setupPanel) {
    state.training_session_panel = setupPanel;
  },
  setTireDialogState(state, tireState) {
    state.tire_dialog = tireState;
  },
  resetNavigationState(state) {
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
