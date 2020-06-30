import Vue from 'vue';
import VueLodash from 'vue-lodash';
import cloneDeep from 'lodash/cloneDeep';
import uniq from 'lodash/uniq';
import mapValues from 'lodash/mapValues';
import orderBy from 'lodash/orderBy';

Vue.use(VueLodash, {
  lodash: {
    cloneDeep,
    uniq,
    mapValues,
    orderBy,
  },
});

export default new VueLodash();
