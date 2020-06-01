import Vue from 'vue';
import VueRouter from 'vue-router';
import VueMeta from 'vue-meta';
import Dashboard from '../components/Dashboard.vue';
import Maintenance from '../components/Maintenance.vue';
import History from '../components/History.vue';

Vue.use(VueRouter);
Vue.use(VueMeta, {
  refreshOnceOnNavigation: true,
});

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/dashboard',
      alias: '/',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: Maintenance,
    },
    {
      path: '/history',
      name: 'History',
      component: History,
    },
  ],
});
