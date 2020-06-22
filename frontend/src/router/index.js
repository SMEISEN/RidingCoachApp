import Vue from 'vue';
import VueRouter from 'vue-router';
import VueMeta from 'vue-meta';
import Dashboard from '../pages/DashboardPage';
import Maintenance from '../pages/MaintenancePage';
import History from '../pages/HistoryPage';
import Login from '../components/Login.vue';
import store from '../store';

Vue.use(VueRouter);
Vue.use(VueMeta, {
  refreshOnceOnNavigation: true,
});

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
  } else {
    next('/dashboard');
  }
};
const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
  } else {
    next('/login');
  }
};


export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      alias: '/',
      name: 'Login',
      component: Login,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: Maintenance,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/history',
      name: 'History',
      component: History,
      beforeEnter: ifAuthenticated,
    },
  ],
});
