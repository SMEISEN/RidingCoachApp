import Vue from 'vue';
import VueRouter from 'vue-router';
import History from '../components/History.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      alias: '/home',
      name: 'History',
      component: History,
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
      name: 'History',
      component: History,
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
