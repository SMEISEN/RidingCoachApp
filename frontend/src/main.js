import Vue from 'vue';
import app from './App.vue';
import router from './router/index';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(app),
}).$mount('#app');
