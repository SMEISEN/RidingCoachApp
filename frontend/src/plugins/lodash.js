import Vue from 'vue';
import VueLodash from 'vue-lodash';
import cloneDeep from 'lodash/cloneDeep';
import uniq from 'lodash/uniq';
import map from 'lodash/map';
import mapValues from 'lodash/mapValues';
import orderBy from 'lodash/orderBy';
import flatten from 'lodash/flatten';
import mean from 'lodash/mean';
import min from 'lodash/min';

Vue.use(VueLodash, {
  lodash: {
    cloneDeep,
    uniq,
    map,
    mapValues,
    orderBy,
    flatten,
    mean,
    min,
  },
});

export default new VueLodash();
