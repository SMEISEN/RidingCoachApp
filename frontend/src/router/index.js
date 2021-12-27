import Vue from 'vue';
import VueRouter from 'vue-router';
import VueMeta from 'vue-meta';
import Dashboard from '../pages/DashboardPage/index.vue';
import Maintenance from '../pages/MaintenancePage/index.vue';
import Spareparts from '../pages/SparepartsPage/index.vue';
import Training from '../pages/TrainingPage/index.vue';
import History from '../pages/HistoryPage/index.vue';
import Login from '../pages/LoginPage/index.vue';
import NotFound from '../pages/NotFound/index.vue';
import store from '../store';

// Use the vue router, setup authentication, define page routes, and export the setup
Vue.use(VueRouter);
Vue.use(VueMeta, {
  refreshOnceOnNavigation: true,
});

/**
 * Proceed to the login page if the user is not authenticated, otherwise, proceed to the dashboard
 * page.
 * @param {object} to
 * @param {object} from
 * @param {function} next
 */
const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    // do nothing
    next();
  } else {
    // proceed to dashboard page
    next('/dashboard');
  }
};
/**
 * Proceed to the requested page if the user is authenticated, otherwise, proceed to the login page.
 * @param {object} to
 * @param {object} from
 * @param {function} next
 */
const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    // do nothing
    next();
  } else {
    // proceed to login page
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
      path: '/spareparts',
      name: 'Spare Parts',
      component: Spareparts,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/training',
      name: 'Training',
      component: Training,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/history',
      name: 'History',
      component: History,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '*',
      name: 'Page not found',
      component: NotFound,
      beforeEnter: ifAuthenticated,
    },
  ],
});
