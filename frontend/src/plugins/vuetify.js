import Vue from 'vue';
import Vuetify from 'vuetify';
import de from 'vuetify/es5/locale/de';
import 'vuetify/dist/vuetify.min.css';
import '@mdi/font/css/materialdesignicons.css';
import 'roboto-fontface/css/roboto/roboto-fontface.css';

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
        error: '#FF5252',
        info: '#8E24AA',
        success: '#4CAF50',
        warning: '#FFC107',
      },
    },
  },
  lang: {
    locales: { de },
    current: 'de',
  },
  icons: {
    iconfont: 'mdi',
  },
});
