import Vue from 'vue';
import 'moment';
import moment from 'moment-timezone';

// Do not show production tips
Vue.config.productionTip = false;
// Filter date time strings by guessing the time zone and transforming to the defined format.
Vue.filter('formatDateTime', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('YYYY-MM-DD HH:mm');
  }
  return console.log('Date format filter failed!');
});
// Filter date strings by guessing the time zone and transforming to the defined format.
Vue.filter('formatDate', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('YYYY-MM-DD');
  }
  return console.log('Date format filter failed!');
});
// Filter time strings by guessing the time zone and transforming to the defined format.
Vue.filter('formatTime', (value) => {
  if (value) {
    const timezone = moment.tz.guess();
    return moment.utc(String(value)).tz(timezone).format('HH:mm');
  }
  return console.log('Date format filter failed!');
});
Vue.prototype.$publicPath = process.env.BASE_URL;
