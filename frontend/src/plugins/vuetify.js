import Vue from 'vue';
import Vuetify from 'vuetify';
import en from 'vuetify/es5/locale/en';
/*import 'vuetify/dist/vuetify.min.css';
import '@mdi/font/css/materialdesignicons.css';
import 'roboto-fontface/css/roboto/roboto-fontface.css';*/

// Use vuetify, define color themes, language, and icons, and export the setup
Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: '#0D47A1',
        secondary: '#1E88E5',
        accent: '#82B1FF',
        error: '#F44336',
        info: '#9C27B0',
        success: '#4CAF50',
        warning: '#FFC107',
        neutral: '#9E9E9E',
      },
    },
  },
  lang: {
    locales: { en },
    current: 'en',
  },
  icons: {
    iconfont: 'mdi',
  },
});
