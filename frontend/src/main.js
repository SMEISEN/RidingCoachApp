import Vue from 'vue';
import 'moment';
import moment from 'moment-timezone';
import vuetify from './plugins/vuetify';
import App from './App.vue';
import router from './router/index';

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
  render: (h) => h(App),
}).$mount('#app');
