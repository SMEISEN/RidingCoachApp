<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      hide-on-scroll
      dense
      v-if="isAuthenticated"
    >

      <v-app-bar-nav-icon @click="navigationDrawer()"></v-app-bar-nav-icon>

      <v-tabs
        grow
        right
        dark
      >
        <v-tabs-slider color="accent"></v-tabs-slider>

        <v-tab to="/dashboard">
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
                           v-touch="{ right: () => editBike(bike.bike_id) }"
              >
                <v-list-item-action>
                  <v-radio :value="bike.bike_id" :key="bike.bike_id"></v-radio>
                </v-list-item-action>
                <v-list-item-title>
                  {{ bike.manufacturer }} {{ bike.model }} {{ bike.year }}
                </v-list-item-title>
                <v-list-item-icon @click="editBike(bike.bike_id)">
                  <v-icon>mdi-settings</v-icon>
                </v-list-item-icon>
              </v-list-item>
              <v-list-item @click="createBike()">
                <v-list-item-action>
                  <v-icon>mdi-plus</v-icon>
                </v-list-item-action>
                <v-list-item-action-text>
                  Add new bike
                </v-list-item-action-text>
              </v-list-item>
            </v-radio-group>
          </v-list-group>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-dumbbell</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Training
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-medical-bag</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Spare parts
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-settings</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Settings
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="onLogout">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Logout
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-dialog v-model="bike_dialog" fullscreen hide-overlay
                transition="dialog-bottom-transition">
        <v-form
          v-model="valid"
          ref="validation_form"
        >
          <v-card>
            <v-toolbar dark color="primary">
              <v-btn icon dark @click="onCancel">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-toolbar-title>Motorbike settings</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn dark text @click="confirm_delete_dialog = true">Delete</v-btn>
              </v-toolbar-items>
              <v-toolbar-items>
                <v-btn dark text @click="onSubmit" :disabled="!valid">Save</v-btn>
              </v-toolbar-items>
            </v-toolbar>
            <v-subheader>Required fields</v-subheader>
            <v-card-text>
              <v-row dense>
                <v-col cols="12" xs="12" sm="4" md="4">
                  <v-text-field
                    label="Manufacturer*"
                    :rules="[v => !!v]"
                    required
                    v-model="bike_form_dict.manufacturer"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="5" md="5">
                  <v-text-field
                    label="Model*"
                    :rules="[v => !!v]"
                    required
                    v-model="bike_form_dict.model"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="3" md="3">
                  <v-text-field
                    append-outer-icon="mdi-plus"
                    prepend-icon="mdi-minus"
                    @click:append-outer="incrementYear"
                    @click:prepend="decrementYear"
                    :rules="[v => !!v]"
                    required
                    label="Year*"
                    v-model="bike_form_dict.year"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="9" md="9"></v-col>
                <v-col cols="12" xs="12" sm="3" md="3">
                  <v-text-field
                    append-outer-icon="mdi-plus"
                    prepend-icon="mdi-minus"
                    @click:append-outer="incrementHour"
                    @click:prepend="decrementHour"
                    :rules="[v => !!v]"
                    required
                    hint="of engine operation"
                    suffix="h*"
                    v-model="bike_form_dict.operating_hours">
                  </v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-divider></v-divider>
            <v-subheader>Optional fields</v-subheader>
            <v-card-text>
              <v-row dense>
                <v-col cols="12" xs="4" sm="4" md="4">
                  <v-text-field
                    label="Engine ccm"
                    v-model="bike_form_dict.ccm"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="4" sm="4" md="4">
                  <v-text-field
                    label="Engine stroke"
                    v-model="bike_form_dict.stroke"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="4" sm="4" md="4">
                  <v-text-field
                    label="Engine piston"
                    v-model="bike_form_dict.piston"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="6" md="6">
                  <v-text-field
                    label="Slick front"
                    v-model="bike_form_dict.slick_front"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="6" md="6">
                  <v-text-field
                    label="Slick rear"
                    v-model="bike_form_dict.slick_rear"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="6" md="6">
                  <v-text-field
                    label="Rain front"
                    v-model="bike_form_dict.rain_front"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="6" md="6">
                  <v-text-field
                    label="Rain rear"
                    v-model="bike_form_dict.rain_rear"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-form>
      </v-dialog>
      <v-dialog v-model="confirm_delete_dialog" persistent max-width="400">
        <v-card>
          <v-card-title class="headline">
            Warning
          </v-card-title>
          <v-card-text>
            <p class="text--primary">
              Do you really want to delete this bike?</p>
            <p class="text--secondary text-sm-left">
              The deletion is permanent and cannot be undone.</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="accent" text
                   @click="confirm_delete_dialog = false">Cancel</v-btn>
            <v-btn color="error" text
                   @click="deleteBikeData()">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios';
import { AUTH_LOGOUT } from './store/actions/authentication';

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
    bike_dialog: false,
    confirm_delete_dialog: false,
    selected_bike: '',
    bike_list: [],
    bike_form_dict: {
      bike_id: null,
      manufacturer: null,
      model: null,
      year: null,
      operating_hours: null,
      ccm: null,
      stroke: null,
      piston: null,
      slick_front: null,
      slick_rear: null,
      rain_front: null,
      rain_rear: null,
      setup: null,
    },
    active_tr: false,
    navigation_drawer: false,
    collapse_bar: false,
    valid: true,
    edit: false,
  }),
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    getBikeData() {
      const ApiPath = '/api/bike';
      axios.get(ApiPath)
        .then((res) => {
          this.bike_list = res.data;
          if (this.$store.getters.getCurrentBikeId === null) {
            this.selectBike(0);
          } else {
            this.selected_bike = this.$store.getters.getCurrentBikeId;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    postBikeData(payload) {
      const ApiPath = '/api/bike';
      axios.post(ApiPath, payload)
        .then(() => {
          this.getBikeData();
        })
        .catch((error) => {
          console.error(error);
          this.getBikeData();
        });
    },
    putBikeData(BikeId, payload) {
      const ApiPath = `/api/bike/${BikeId}`;
      axios.put(ApiPath, payload)
        .then(() => {
          this.getBikeData();
          this.selected_bike = BikeId;
        })
        .catch((error) => {
          console.error(error);
          this.getBikeData();
          this.selected_bike = BikeId;
        });
    },
    deleteBikeData() {
      const ApiPath = `/api/bike/${this.bike_form_dict.bike_id}`;
      axios.delete(ApiPath)
        .then(() => {
          this.getBikeData();
        })
        .catch((error) => {
          console.error(error);
          this.getBikeData();
        });
      this.confirm_delete_dialog = false;
      this.bike_dialog = false;
      this.initForm();
    },
    selectBike(index) {
      const selectedBike = this.bike_list[index];
      this.selected_bike = selectedBike.bike_id;
      this.$store.commit('selectBike', selectedBike);
      this.$forceUpdate();
    },
    navigationDrawer() {
      this.navigation_drawer = true;
      this.collapse_bar = false;
    },
    createBike() {
      this.bike_dialog = true;
      this.navigation_drawer = false;
    },
    editBike(BikeId) {
      for (let i = 0; i < this.bike_list.length; i += 1) {
        if (Object.values(this.bike_list[i]).includes(BikeId)) {
          this.bike_form_dict.bike_id = this.bike_list[i].bike_id;
          this.bike_form_dict.manufacturer = this.bike_list[i].manufacturer;
          this.bike_form_dict.model = this.bike_list[i].model;
          this.bike_form_dict.year = this.bike_list[i].year;
          this.bike_form_dict.operating_hours = this.bike_list[i].operating_hours;
          this.bike_form_dict.ccm = this.bike_list[i].ccm;
          this.bike_form_dict.stroke = this.bike_list[i].stroke;
          this.bike_form_dict.piston = this.bike_list[i].piston;
          this.bike_form_dict.slick_front = this.bike_list[i].slick_front;
          this.bike_form_dict.slick_rear = this.bike_list[i].slick_rear;
          this.bike_form_dict.rain_front = this.bike_list[i].rain_front;
          this.bike_form_dict.rain_rear = this.bike_list[i].rain_rear;
          this.bike_form_dict.setup = this.bike_list[i].setup;
        }
      }
      this.edit = true;
      this.bike_dialog = true;
      this.navigation_drawer = false;
    },
    incrementHour() {
      this.bike_form_dict.operating_hours = Number(
        parseFloat(this.bike_form_dict.operating_hours) + 0.1,
      ).toFixed(1);
    },
    decrementHour() {
      this.bike_form_dict.operating_hours = Number(
        parseFloat(this.bike_form_dict.operating_hours) - 0.1,
      ).toFixed(1);
    },
    incrementYear() {
      this.bike_form_dict.year = Number(
        parseFloat(this.bike_form_dict.year) + 1,
      ).toFixed(0);
    },
    decrementYear() {
      this.bike_form_dict.year = Number(
        parseFloat(this.bike_form_dict.year) - 1,
      ).toFixed(0);
    },
    onSubmit(evt) {
      evt.preventDefault();
      const BikeId = this.bike_form_dict.bike_id;
      const payload = {
        operating_hours: this.bike_form_dict.operating_hours,
        manufacturer: this.bike_form_dict.manufacturer,
        model: this.bike_form_dict.model,
        year: this.bike_form_dict.year,
        ccm: this.bike_form_dict.ccm,
        stroke: this.bike_form_dict.stroke,
        piston: this.bike_form_dict.piston,
        slick_front: this.bike_form_dict.slick_front,
        slick_rear: this.bike_form_dict.slick_rear,
        rain_front: this.bike_form_dict.rain_front,
        rain_rear: this.bike_form_dict.rain_rear,
        setup: this.bike_form_dict.setup,
      };
      if (this.edit === false) {
        this.postBikeData(payload);
      } else {
        this.putBikeData(BikeId, payload);
        if (this.selected_bike === BikeId) {
          payload.bike_id = BikeId;
          this.$store.commit('selectBike', payload);
          this.$forceUpdate();
        }
      }
      this.bike_dialog = false;
      this.initForm();
    },
    onCancel(evt) {
      evt.preventDefault();
      this.bike_dialog = false;
      this.initForm();
    },
    onLogout() {
      this.$store.dispatch(AUTH_LOGOUT);
      this.$router.push('/login');
    },
    initForm() {
      this.bike_form_dict.manufacturer = null;
      this.bike_form_dict.model = null;
      this.bike_form_dict.year = null;
      this.bike_form_dict.ccm = null;
      this.bike_form_dict.stroke = null;
      this.bike_form_dict.piston = null;
      this.bike_form_dict.slick_front = null;
      this.bike_form_dict.slick_rear = null;
      this.bike_form_dict.rain_front = null;
      this.bike_form_dict.rain_rear = null;
      this.bike_form_dict.setup = null;
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
      this.edit = false;
    },
  },
  created() {
    this.getBikeData();
  },
  updated() {
  },
};
</script>

<style>
  html { overflow-y: auto }
</style>
