/* eslint no-shadow: ["error", { "allow": ["state"] }] */

const getDefaultState = () => ({
  sparepart_id: null,
});
const state = getDefaultState();
const getters = {
  getSparepartId: (state) => state.sparepart_id,
};
const mutations = {
  setSparepartId(state, sparepartId) {
    state.sparepart_id = sparepartId;
  },
};
const actions = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
