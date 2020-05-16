import Vue from 'vue';
import VueRouter from 'vue-router';
import Maintenance from '../components/Maintenance.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      alias: '/home',
      name: 'Maintenance',
      component: Maintenance,
      meta: {
        title: 'Home Page - Example App',
        metaTags: [
          {
            name: 'description',
            content: 'The home page of our example app.',
          },
          {
            property: 'og:description',
            content: 'The home page of our example app.',
          },
        ],
      },
    },
    {
      path: '/index.html',
      name: 'Maintenance',
      component: Maintenance,
      meta: {
        title: 'Home Page - Example App',
        metaTags: [
          {
            name: 'description',
            content: 'The home page of our example app.',
          },
          {
            property: 'og:description',
            content: 'The home page of our example app.',
          },
        ],
      },
    },
  ],
});
