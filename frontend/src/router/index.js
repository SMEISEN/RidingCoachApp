import Vue from 'vue';
import VueRouter from 'vue-router';
import Maintenance from '../components/Maintenance.vue';

Vue.use(VueRouter);

export default new VueRouter({
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Maintenance',
      component: Maintenance,
    },
  ],
});
