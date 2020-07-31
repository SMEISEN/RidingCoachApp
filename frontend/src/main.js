import Vue from 'vue';
import './plugins/config';
import vuetify from './plugins/vuetify';
import lodash from './plugins/lodash';
import router from './router/index';
import store from './store';
import App from './App.vue';

new Vue({
  router,
  vuetify,
  lodash,
  store,
  render: (h) => h(App),
}).$mount('#app');
