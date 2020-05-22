import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import Maintenance from '../components/Maintenance.vue';
import History from '../components/History.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/dashboard',
      alias: '/home',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        title: 'Dashboard',
        metaTags: [
          {
            name: 'Dashboard',
            content: 'tbd',
          },
          {
            property: 'og:tbd',
            content: 'tbd',
          },
        ],
      },
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: Maintenance,
      meta: {
        title: 'Maintenance',
        metaTags: [
          {
            name: 'description',
            content: 'tbd',
          },
          {
            property: 'og:tbd',
            content: 'tbd',
          },
        ],
      },
    },
    {
      path: '/history',
      name: 'History',
      component: History,
      meta: {
        title: 'History',
        metaTags: [
          {
            name: 'History',
            content: 'tbd',
          },
          {
            property: 'og:tbd',
            content: 'tbd',
          },
        ],
      },
    },
    {
      path: '/index.html',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        title: 'Dashboard',
        metaTags: [
          {
            name: 'Dashboard',
            content: 'tbd',
          },
          {
            property: 'og:tbd',
            content: 'tbd',
          },
        ],
      },
    },
  ],
});
