import App from '@/App.vue';
import router from '@/router';
import vuetify from '@/plugins/vuetify';
import lodash from '@/plugins/lodash';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import store from '@/store';
import {
  AUTH_LOGOUT,
  AUTH_REQUEST} from '@/store/actions/authentication';
import {
  mount,
  createLocalVue
} from '@vue/test-utils';

const { isNavigationFailure, NavigationFailureType } = VueRouter;

const localVue = createLocalVue();
localVue.use(VueRouter);
localVue.use(Vuex);
localVue.use(Vuetify);

const username = process.env.VUE_APP_USER;
const password = process.env.VUE_APP_SECRET;

let wrapper;

beforeEach(() => {
  wrapper = mount(App, {
    localVue,
    vuetify,
    router,
    store
  });
});

afterEach(() => {
  wrapper.destroy();
});

describe('render pages while user is not logged in', () => {

  beforeEach(async () => {
    store.dispatch(AUTH_LOGOUT);
    await wrapper.vm.$nextTick();
  });

  it('renders the login page',
    async () => {

      router.push('/login').catch(err => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page, alias path',
    async () => {

      router.push('/').catch(err => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page because of navigation guard redirection',
    async () => {

      router.push('/dashboard').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page because of navigation guard redirection',
    async () => {

      router.push('/maintenance').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page because of navigation guard redirection',
    async () => {

      router.push('/spareparts').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page because of navigation guard redirection',
    async () => {

      router.push('/training').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page because of navigation guard redirection',
    async () => {

      router.push('/history').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });
});

describe('render pages while user is logged in', () => {

  beforeEach(async () => {
    store.dispatch(AUTH_REQUEST, { username, password });
    await wrapper.vm.$nextTick();
  });

  it('renders the login page',
    async () => {

      router.push('/login').catch(err => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/login');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the login page, alias path',
    async () => {

      router.push('/').catch(err => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/');
      expect(wrapper.findComponent({name: 'Login'}).exists()).toBe(true);
    });

  it('renders the the dashboard page',
    async () => {

      router.push('/dashboard').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/dashboard');
      expect(wrapper.findComponent({ name: 'Dashboard' }).exists()).toBe(true);
    });

  it('renders the the maintenance page',
    async () => {

      router.push('/maintenance').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/maintenance');
      expect(wrapper.findComponent({ name: 'Maintenance' }).exists()).toBe(true);
    });

  it('renders the the spareparts page',
    async () => {

      router.push('/spareparts').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/spareparts');
      expect(wrapper.findComponent({ name: 'Spareparts' }).exists()).toBe(true);
    });

  it('renders the the training page',
    async () => {

      router.push('/training').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/training');
      expect(wrapper.findComponent({ name: 'Training' }).exists()).toBe(true);
    });

  it('renders the the history page',
    async () => {

      router.push('/history').catch((e) => {
        if (!isNavigationFailure(e, NavigationFailureType.redirected)) {
          Promise.reject(e)
        }
      })
      await wrapper.vm.$nextTick();

      expect(router.history.current.path).toEqual('/history');
      expect(wrapper.findComponent({ name: 'History' }).exists()).toBe(true);
    });
});
