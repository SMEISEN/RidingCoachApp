import Vue from 'vue';
import 'moment';
import moment from 'moment-timezone';

Vue.config.productionTip = false;
Vue.filter('formatDateTime', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('YYYY-MM-DD HH:mm');
  }
  return console.log('Date format filter failed!');
});
Vue.prototype.$publicPath = process.env.BASE_URL;
