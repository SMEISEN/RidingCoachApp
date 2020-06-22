/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const state = () => ({
  history_edit_flag: false,
  history_add_or_edit_dialog: false,
});
const getters = {
  getHistoryEditFlag: (state) => state.history_edit_flag,
  getHistoryAddOrEditDialog: (state) => state.history_add_or_edit_dialog,
};
const mutations = {
  setHistoryEditFlag(state, editFlag) {
    state.history_edit_flag = editFlag;
  },
  setHistoryAddOrEditDialog(state, editDialog) {
    state.history_add_or_edit_dialog = editDialog;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
