/* eslint no-shadow: ["error", { "allow": ["state"] }] */
import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT,
} from '../actions/authentication';
import { apiLogin } from '../../components/api/LoginApi';

const getDefaultState = () => ({
  token: '',
  status: '',
  hasLoadedOnce: false,
});
const state = getDefaultState();
const getters = {
  isAuthenticated: (state) => !!state.token,
  authStatus: (state) => state.status,
};
const actions = {
  [AUTH_REQUEST]: ({ commit }, user) => new Promise((resolve, reject) => {
    commit(AUTH_REQUEST);
    apiLogin({ url: 'auth', data: user, method: 'POST' })
      .then((resp) => {
        localStorage.setItem('user-token', resp.token);
        // Here set the header of your ajax library to the token value.
        // example with axios
        // axios.defaults.headers.common['Authorization'] = resp.token
        commit(AUTH_SUCCESS, resp);
        resolve(resp);
      })
      .catch((err) => {
        commit(AUTH_ERROR, err);
        localStorage.removeItem('user-token');
        reject(err);
      });
  }),
  [AUTH_LOGOUT]: ({ commit }) => new Promise((resolve) => {
    commit(AUTH_LOGOUT);
    localStorage.removeItem('user-token');
    resolve();
  }),
};
const mutations = {
  [AUTH_REQUEST]: (state) => {
    state.status = 'loading';
  },
  [AUTH_SUCCESS]: (state, resp) => {
    state.status = 'success';
    state.token = resp.token;
    state.hasLoadedOnce = true;
  },
  [AUTH_ERROR]: (state) => {
    state.status = 'error';
    state.hasLoadedOnce = true;
  },
  [AUTH_LOGOUT]: (state) => {
    state.token = '';
  },
  resetAuthenticationState(state) {
    Object.assign(state, getDefaultState());
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
