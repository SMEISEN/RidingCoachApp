import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';
import bike from './modules/bike';
import authentication from './modules/authentication';
import history from './modules/history';
import navigation from './modules/navigation';
import info from './modules/info';

Cookies.defaults = {
  sameSite: 'None',
  Secure: true,
};

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    bike,
    authentication,
    history,
    navigation,
    info,
  },
  plugins: [createPersistedState({
    paths: ['authentication.token'],
    storage: {
      getItem: (key) => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 90, secure: true }),
      removeItem: (key) => Cookies.remove(key),
    },
  })],
});
