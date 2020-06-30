import Vue from 'vue';
import 'moment';
import moment from 'moment-timezone';
import vuetify from './plugins/vuetify';
import lodash from './plugins/lodash';
import App from './App.vue';
import router from './router/index';
import store from './store';

Vue.config.productionTip = false;
Vue.filter('formatDateTime', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('YYYY-MM-DD HH:mm');
  }
  return console.log('Date format filter failed!');
});

new Vue({
  router,
  vuetify,
  lodash,
  store,
  render: (h) => h(App),
}).$mount('#app');
