import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';
import bike from './modules/bike';
import authentication from './modules/authentication';
import history from './modules/history'
import navigation from './modules/navigation'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    bike,
    authentication,
    history,
    navigation,
  },
  plugins: [createPersistedState({
    storage: {
      getItem: (key) => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 90, secure: true }),
      removeItem: (key) => Cookies.remove(key),
    },
  })],
});
