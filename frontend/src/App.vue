<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      hide-on-scroll
      :collapse="collapse_bar"
      dense
    >

      <v-app-bar-nav-icon @click="navigationDrawer()"></v-app-bar-nav-icon>

      <v-tabs
        grow
        right
        dark
        v-touch="{ right: () => this.collapse_bar = false }"
      >
        <v-tabs-slider color="accent"></v-tabs-slider>

        <v-tab to="/">
          Dashboard
        </v-tab>
        <v-tab to="/maintenance">
          Maintenance
        </v-tab>
        <v-tab to="/history">
          History
        </v-tab>

      </v-tabs>

    </v-app-bar>

    <v-content>
      <router-view></router-view>
      <v-navigation-drawer
        v-model="navigation_drawer"
        absolute
        temporary
        width="auto"
      >
        <v-list>
          <v-list-group
            prepend-icon="mdi-motorbike"
            nav
            dense
            active-class="primary--text text--accent"
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Bike</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-radio-group v-model="selected_bike">
             <v-list-item v-for="(bike, index) in bike_list" :key="index"
                          @click="selectBike(index)"
                          v-touch="{ right: () => {editBike} }">
               <v-list-item-action>
                 <v-radio :value="bike.bike_id" :key="bike.bike_id"></v-radio>
               </v-list-item-action>
               <v-list-item-title>
                 {{ bike.manufacturer }} {{ bike.model }} {{ bike.year }}
               </v-list-item-title>
              <v-list-item-icon to="/" @click="editBike(bike.bike_id)">
                <v-icon>mdi-settings</v-icon>
              </v-list-item-icon>
            </v-list-item>
            </v-radio-group>
          </v-list-group>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-icon>
                <v-icon>mdi-settings</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Settings</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-content>
  </v-app>
</template>

<script>

import axios from 'axios';

export default {
  name: 'App',
  metaInfo: {
    titleTemplate: '%s | Riding Coach',
    meta: [
      { name: 'viewport', content: 'width=device-width' },
      { name: 'mobile-web-app-capable', content: 'yes' },
    ],
    link: [
      { rel: 'shortcut icon', type: 'image/svg', href: '/rc-logo.svg' },
    ],
  },

  data: () => ({
    selected_bike: '',
    bike_list: [],
    active_tr: false,
    navigation_drawer: false,
    collapse_bar: false,
  }),
  methods: {
    getBikeData() {
      const ApiPath = '/api/bike';
      axios.get(ApiPath).then((res) => {
        this.bike_list = res.data;
      });
    },
    selectBike(index) {
      const selectedBike = this.bike_list[index];
      this.selected_bike = selectedBike.bike_id;
      this.$store.commit('selectBike', selectedBike);
    },
    editBike() {
      this.collapse_bar = true;
      this.navigation_drawer = false;
    },
    navigationDrawer() {
      this.navigation_drawer = true;
      this.collapse_bar = false;
    },
  },
  created() {
    this.getBikeData();
    if (this.$store.getters.getCurrentBikeId === 'undefined') {
      this.selectBike(0);
    }
    this.selected_bike = this.$store.getters.getCurrentBikeId;
  },
  updated() {
  },
};
</script>
