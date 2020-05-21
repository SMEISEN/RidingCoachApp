import Vue from 'vue';
import vuetify from '@/plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@mdi/font/css/materialdesignicons.css';
import 'moment';
import moment from 'moment-timezone';

import App from './App.vue';
import router from './router/index';

Vue.config.productionTip = false;
Vue.filter('formatDate', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('MM/DD/YYYY HH:mm');
  }
  return console.log('Date format filter failed!');
});

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
