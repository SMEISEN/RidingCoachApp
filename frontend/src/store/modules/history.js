/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  history_edit_flag: false,
  history_add_or_edit_dialog: false,
  history_id: null,
});
const state = getDefaultState();
const getters = {
  getHistoryEditFlag: (state) => state.history_edit_flag,
  getHistoryAddOrEditDialog: (state) => state.history_add_or_edit_dialog,
  getHistoryId: (state) => state.history_id,
};
const mutations = {
  setHistoryEditFlag(state, editFlag) {
    state.history_edit_flag = editFlag;
  },
  setHistoryAddOrEditDialog(state, editDialog) {
    state.history_add_or_edit_dialog = editDialog;
  },
  setHistoryId(state, histId) {
    state.history_id = histId;
  },
  resetHistoryState(state) {
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
