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
        style="position:fixed; top:48px; left:0;"
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
            <v-radio-group v-model="selected_bike.bike_id">
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
          <v-list-item @click="editTraining">
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
          v-model="valid_bike_dialog"
          ref="validation_bike_form"
        >
          <v-card>
            <v-toolbar dark color="primary">
              <v-btn icon dark @click="onBikeCancel">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-toolbar-title>Motorbike settings</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn dark text @click="confirm_delete_dialog = true">Delete</v-btn>
              </v-toolbar-items>
              <v-toolbar-items>
                <v-btn dark text @click="onBikeSubmit" :disabled="!valid_bike_dialog">Save</v-btn>
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
                <v-col cols="12" xs="12" sm="5" md="6">
                  <v-text-field
                    label="Model*"
                    :rules="[v => !!v]"
                    required
                    v-model="bike_form_dict.model"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="3" md="2">
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
                <v-col cols="12" xs="12" sm="9" md="10"></v-col>
                <v-col cols="12" xs="12" sm="3" md="2">
                  <v-text-field
                    append-outer-icon="mdi-plus"
                    prepend-icon="mdi-minus"
                    @click:append-outer="incrementHour"
                    @click:prepend="decrementHour"
                    :rules="[v => !!v]"
                    required
                    label="Operating hours*"
                    hint="of engine"
                    suffix="h"
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
            <v-divider></v-divider>
            <v-subheader>Available setup</v-subheader>
            <v-card-text>
              <v-simple-table dense light>
                <thead>
                <tr>
                  <th class="text-left">Category</th>
                  <th class="text-left">Name</th>
                  <th class="text-left">Available ticks</th>
                  <th class="text-left">Standard tick</th>
                </tr>
                </thead>
                <tbody>
                  <tr v-for="(entry, index) in bike_form_dict.setup_individual"
                      v-bind:key="index">
                    <td style="border-bottom: none"><v-text-field
                        style="font-size: 12px"
                        dense
                        height="20px"
                        v-model="entry.category"
                        single-line />
                    </td>
                    <td style="border-bottom: none"><v-text-field
                        style="font-size: 12px"
                        dense
                        height="20px"
                        v-model="entry.name"
                        single-line />
                    </td>
                    <td style="border-bottom: none"><v-text-field
                        style="font-size: 12px"
                        dense
                        height="20px"
                        v-model="entry.ticks_available"
                        single-line />
                    </td>
                    <td style="border-bottom: none"><v-text-field
                        style="font-size: 12px"
                        dense
                        height="20px"
                        v-model="entry.ticks_standard"
                        single-line />
                    </td>
                  </tr>
                </tbody>
              </v-simple-table>
            </v-card-text>
            <v-card-text style="height: 50px; position: relative">
              <v-btn
                absolute
                small
                fab
                top
                right
                color="primary"
                @click="addSetupRow"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
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
      <v-dialog v-model="training_dialog" fullscreen hide-overlay
                transition="dialog-bottom-transition">
        <v-form
          v-model="valid_training_dialog"
          ref="validation_training_form"
        >
          <v-card>
            <v-toolbar dark color="primary">
              <v-btn icon dark @click="onTrainingCancel">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-toolbar-title>Training settings</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn dark text @click="onTrainingSubmit" :disabled="!valid_training_dialog">
                  Save
                </v-btn>
              </v-toolbar-items>
            </v-toolbar>
            <v-card-text>
              <v-expansion-panels
                focusable
                v-model="training_general_panel"
              >
                <v-expansion-panel>
                  <v-expansion-panel-header>Location</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-row>
                      <v-col cols="12" xs="12" sm="9" md="10">
                        <v-combobox
                          label="Race track*"
                          :rules="[v => !!v]"
                          required
                          v-model="training_form_dict.race_track"
                        ></v-combobox>
                      </v-col>
                      <v-col cols="auto" xs="12" sm="3" md="2">
                        <v-menu
                          v-model="date_menu"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          scrollable
                          transition="scale-transition"
                          offset-y
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on }">
                            <v-text-field
                              v-model="training_form_dict.date"
                              prepend-icon="mdi-calendar"
                              required
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker v-model="training_form_dict.date"
                                         @input="date_menu = false">
                          </v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                  </v-expansion-panel-content>
                </v-expansion-panel>
                <v-expansion-panel>
                  <v-expansion-panel-header>Weather</v-expansion-panel-header>
                  <v-expansion-panel-content>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>
            <v-tabs
              v-model="training_setup_tab"
              background-color="secondary"
              dark
            >
              <v-tab
                v-for="tab_index in training_setup_tabs"
                :key="tab_index"
              >
                Setup {{ tab_index }}
              </v-tab>
              <v-tab-item
                v-for="tab_item_index in training_setup_tabs"
                :key="tab_item_index"
              >
                <v-card-text>
                  <v-expansion-panels
                    popout
                    focusable
                    v-model="training_setup_panel"
                  >
                    <v-expansion-panel>
                      <v-expansion-panel-header>Engine</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <v-row dense align="start">
                          <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                          <v-col cols="11" xs="11" sm="4" md="4">
                            <v-subheader>Operating hours*</v-subheader>
                            <v-text-field
                              dense
                              append-outer-icon="mdi-plus"
                              prepend-icon="mdi-minus"
                              @click:append-outer="incrementHour(tab_item_index-1)"
                              @click:prepend="decrementHour(tab_item_index-1)"
                              :rules="[v => !!v]"
                              required
                              suffix="h"
                              v-model=
                                "training_form_dict.setup_fixed
                                [tab_item_index-1].operating_hours">
                            </v-text-field>
                          </v-col>
                          <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                          <v-col cols="11" xs="11" sm="4" md="4">
                            <v-subheader>Mode*</v-subheader>
                            <hr style="height:3pt; visibility:hidden;" />
                            <v-slider
                              v-model="engine_mode"
                              :tick-labels="['soft','performance']"
                              :min="1"
                              :max="2"
                              step="1"
                              ticks="always"
                              tick-size="4"
                              append-icon="mdi-plus"
                              prepend-icon="mdi-minus"
                              @click:append="incrementFork2(tab_item_index-1)"
                              @click:prepend="decrementFork2(tab_item_index-1)"
                            >
                            </v-slider>
                          </v-col>
                          <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                        </v-row>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel>
                      <v-expansion-panel-header>Tires</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <br/>
                        <v-window
                          v-model="rain_tires"
                        >
                          <v-window-item>
                            <v-row dense>
                              <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                              <v-col cols="11" xs="11" sm="4" md="4">
                                <v-text-field
                                  append-outer-icon="mdi-plus"
                                  prepend-icon="mdi-minus"
                                  @click:append-outer=
                                    "incrementTirePressureFront(tab_item_index-1)"
                                  @click:prepend=
                                    "decrementTirePressureFront(tab_item_index-1)"
                                  :rules="[v => !!v]"
                                  required
                                  label="Front tire pressure"
                                  suffix="bar"
                                  hint="recommended: 2.1 bar"
                                  persistent-hint
                                  v-model=
                                    "training_form_dict.setup_fixed
                                    [tab_item_index-1].slick_pressure_front">
                                </v-text-field>
                              </v-col>
                              <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                              <v-col cols="11" xs="11" sm="4" md="4">
                                <v-text-field
                                  append-outer-icon="mdi-plus"
                                  prepend-icon="mdi-minus"
                                  @click:append-outer=
                                    "incrementTirePressureRear(tab_item_index-1)"
                                  @click:prepend=
                                    "decrementTirePressureRear(tab_item_index-1)"
                                  :rules="[v => !!v]"
                                  required
                                  label="Rear tire pressure"
                                  suffix="bar"
                                  hint="recommended: 2.1 bar"
                                  persistent-hint
                                  v-model=
                                    "training_form_dict.setup_fixed
                                    [tab_item_index-1].slick_pressure_rear">
                                </v-text-field>
                              </v-col>
                              <v-col cols="11" xs="0" sm="1" md="1"></v-col>
                            </v-row>
                          </v-window-item>
                          <v-window-item>
                            <v-row dense>
                              <v-col cols="12" xs="0" sm="1" md="1"></v-col>
                              <v-col cols="12" xs="12" sm="4" md="4">
                                <v-text-field
                                  append-outer-icon="mdi-plus"
                                  prepend-icon="mdi-minus"
                                  @click:append-outer=
                                    "incrementTirePressureFront(tab_item_index-1)"
                                  @click:prepend=
                                    "decrementTirePressureFront(tab_item_index-1)"
                                  :rules="[v => !!v]"
                                  required
                                  label="Front tire pressure"
                                  suffix="bar"
                                  hint="recommended: 2.1 bar"
                                  persistent-hint
                                  v-model=
                                    "training_form_dict.setup_fixed
                                    [tab_item_index-1].rain_pressure_front">
                                </v-text-field>
                              </v-col>
                              <v-col cols="12" xs="0" sm="2" md="2"></v-col>
                              <v-col cols="12" xs="12" sm="4" md="4">
                                <v-text-field
                                  append-outer-icon="mdi-plus"
                                  prepend-icon="mdi-minus"
                                  @click:append-outer=
                                    "incrementTirePressureRear(tab_item_index-1)"
                                  @click:prepend=
                                    "decrementTirePressureRear(tab_item_index-1)"
                                  :rules="[v => !!v]"
                                  required
                                  label="Rear tire pressure"
                                  suffix="bar"
                                  hint="recommended: 2.1 bar"
                                  persistent-hint
                                  v-model=
                                    "training_form_dict.setup_fixed
                                    [tab_item_index-1].rain_pressure_rear">
                                </v-text-field>
                              </v-col>
                              <v-col cols="12" xs="0" sm="1" md="1"></v-col>
                            </v-row>
                          </v-window-item>
                        </v-window>
                        <br/>
                        <v-divider></v-divider>
                        <v-card-actions>
                          <v-btn
                            :disabled="rain_tires === 0"
                            color="primary"
                            @click="rain_tires--"
                          >
                            Slick
                          </v-btn>
                          <v-spacer></v-spacer>
                          <v-btn
                            :disabled="rain_tires === 1"
                            color="primary"
                            @click="rain_tires++"
                          >
                            Rain
                          </v-btn>
                        </v-card-actions>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel>
                      <v-expansion-panel-header>Suspension</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <v-row dense
                               v-for="(setup_entry, setup_index) in training_form_dict
                               .setup_individual[tab_item_index-1]"
                               v-bind:key="setup_index">
                          <v-col cols="12" xs="12" sm="3" md="2">
                            <v-subheader>{{ setup_entry.name }}</v-subheader>
                            <v-slider
                              v-model="setup_entry.ticks_current"
                              :tick-labels="tickLabels(
                                setup_entry.ticks_standard,
                                setup_entry.ticks_available)"
                              :max="Number.parseInt(setup_entry.ticks_available)"
                              step="1"
                              ticks="always"
                              append-icon="mdi-plus"
                              prepend-icon="mdi-minus"
                              @click:append=
                                "incrementSetup(tab_item_index-1, setup_index)"
                              @click:prepend=
                                "decrementSetup(tab_item_index-1, setup_index)"
                            >
                            </v-slider>
                          </v-col>
                        </v-row>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-card-text>
              </v-tab-item>
              <v-tab @click="addTab">
                <v-icon>mdi-plus</v-icon>
              </v-tab>
              <v-tab-item></v-tab-item>
            </v-tabs>
          </v-card>
        </v-form>
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
    training_dialog: false,
    confirm_delete_dialog: false,
    selected_bike: {
      bike_id: null,
      index: null,
    },
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
      setup_individual: [
        {
          category: null,
          name: null,
          ticks_available: null,
          ticks_standard: null,
          ticks_current: null,
        },
      ],
    },
    training_form_dict: {
      race_track: null,
      date: null,
      setup_fixed: [
        {
          operating_hours: null,
          slick_pressure_front: null,
          slick_pressure_rear: null,
          rain_pressure_front: null,
          rain_pressure_rear: null,
        },
      ],
      setup_individual: [
        [
          {
            category: null,
            name: null,
            ticks_available: null,
            ticks_standard: null,
            ticks_current: null,
          },
        ],
      ],
    },
    setup_individual_dict: {
      category: null,
      name: null,
      ticks_available: null,
      ticks_standard: null,
    },
    setup_fixed_dict: {
      operating_hours: null,
      slick_pressure_front: null,
      slick_pressure_rear: null,
      rain_pressure_front: null,
      rain_pressure_rear: null,
    },
    active_tr: false,
    navigation_drawer: false,
    collapse_bar: false,
    valid_bike_dialog: true,
    valid_training_dialog: true,
    edit: false,
    date_menu: false,
    setup_entries: 1,
    training_setup_tabs: 1,
    training_setup_tab: null,
    training_general_panel: 0,
    training_setup_panel: 0,
    engine_mode: null,
    fork_1: null,
    fork_2: null,
    rain_tires: 0,
  }),
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    tickLabels(standardTick, availableTicks) {
      const tick_labels = []
      for (let i = 0; i < availableTicks; i += 1) {
        if (i === Number.parseInt(standardTick)) {
          tick_labels.push('0');
        } else {
          tick_labels.push('');
        }
      }
      return tick_labels;
    },
    getBikeData() {
      const ApiPath = '/api/bike';
      axios.get(ApiPath)
        .then((res) => {
          this.bike_list = res.data;
          if (this.$store.getters.getCurrentBikeId === null) {
            this.selectBike(0);
          } else {
            this.selected_bike.bike_id = this.$store.getters.getCurrentBikeId;
            this.selected_bike.index = this.indexOfBikeId(this.$store.getters.getCurrentBikeId);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    indexOfBikeId(BikeId) {
      for (let i = 0; i < this.bike_list.length; i += 1) {
        if (Object.values(this.bike_list[i]).includes(BikeId)) {
          return i;
        }
      }
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
    async putBikeData(BikeId, payload) {
      const ApiPath = `/api/bike/${BikeId}`;
      axios.put(ApiPath, payload)
        .then(() => {
          this.getBikeData();
        })
        .catch((error) => {
          console.error(error);
          this.getBikeData();
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
      this.initBikeForm();
    },
    selectBike(index) {
      const selectedBike = this.bike_list[index];
      this.selected_bike.bike_id = selectedBike.bike_id;
      this.selected_bike.index = index;
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
      const bike_index = this.indexOfBikeId(BikeId)
      this.bike_form_dict.bike_id = this.bike_list[bike_index].bike_id;
      this.bike_form_dict.manufacturer = this.bike_list[bike_index].manufacturer;
      this.bike_form_dict.model = this.bike_list[bike_index].model;
      this.bike_form_dict.year = this.bike_list[bike_index].year;
      this.bike_form_dict.operating_hours = this.bike_list[bike_index].operating_hours;
      this.bike_form_dict.ccm = this.bike_list[bike_index].ccm;
      this.bike_form_dict.stroke = this.bike_list[bike_index].stroke;
      this.bike_form_dict.piston = this.bike_list[bike_index].piston;
      this.bike_form_dict.slick_front = this.bike_list[bike_index].slick_front;
      this.bike_form_dict.slick_rear = this.bike_list[bike_index].slick_rear;
      this.bike_form_dict.rain_front = this.bike_list[bike_index].rain_front;
      this.bike_form_dict.rain_rear = this.bike_list[bike_index].rain_rear;
      this.bike_form_dict.setup_individual = this.bike_list[bike_index].setup;
      this.edit = true;
      this.bike_dialog = true;
      this.navigation_drawer = false;
    },
    editTraining() {
      this.training_dialog = true;
      this.initTrainingForm();
    },
    incrementHour(ind) {
      if (this.bike_dialog === true) {
        this.bike_form_dict.operating_hours = Number(
          parseFloat(this.bike_form_dict.operating_hours) + 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].operating_hours = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].operating_hours) + 0.1,
        ).toFixed(1);
      }
    },
    decrementHour(ind) {
      if (this.bike_dialog === true) {
        this.bike_form_dict.operating_hours = Number(
          parseFloat(this.bike_form_dict.operating_hours) - 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].operating_hours = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].operating_hours) - 0.1,
        ).toFixed(1);
      }
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
    incrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_dict.setup_fixed[ind].slick_pressure_front = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].slick_pressure_front) + 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].rain_pressure_front = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].rain_pressure_front) + 0.1,
        ).toFixed(1);
      }
    },
    decrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_dict.setup_fixed[ind].slick_pressure_front = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].slick_pressure_front) - 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].rain_pressure_front = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].rain_pressure_front) - 0.1,
        ).toFixed(1);
      }
    },
    incrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_dict.setup_fixed[ind].slick_pressure_rear = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].slick_pressure_rear) + 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].rain_pressure_rear = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].rain_pressure_rear) + 0.1,
        ).toFixed(1);
      }
    },
    decrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_dict.setup_fixed[ind].slick_pressure_rear = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].slick_pressure_rear) - 0.1,
        ).toFixed(1);
      } else {
        this.training_form_dict.setup_fixed[ind].rain_pressure_rear = Number(
          parseFloat(this.training_form_dict.setup_fixed[ind].rain_pressure_rear) - 0.1,
        ).toFixed(1);
      }
    },
    incrementSetup(tabIndex, setupIndex) {
      this.training_form_dict.setup_individual[tabIndex][setupIndex].ticks_current += 1;
      this.$forceUpdate();
    },
    decrementSetup(tabIndex, setupIndex) {
      this.training_form_dict.setup_individual[tabIndex][setupIndex].ticks_current -= 1;
      this.$forceUpdate();
    },
    async onBikeSubmit(evt) {
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
        setup: this.bike_form_dict.setup_individual,
      };
      if (this.edit === false) {
        await this.postBikeData(payload);
      } else {
        await this.putBikeData(BikeId, payload);
        if (this.selected_bike.bike_id === BikeId) {
          payload.bike_id = BikeId;
          this.$store.commit('selectBike', payload);
          this.$forceUpdate();
        }
      }
      this.bike_dialog = false;
      this.initBikeForm();
    },
    onTrainingSubmit(evt) {
      evt.preventDefault();
    },
    onBikeCancel(evt) {
      evt.preventDefault();
      this.bike_dialog = false;
      this.initBikeForm();
    },
    onTrainingCancel(evt) {
      evt.preventDefault();
      this.training_dialog = false;
      this.training_setup_tabs = 1;
      this.training_setup_tab = null;
      this.initTrainingForm();
    },
    onLogout() {
      this.$store.dispatch(AUTH_LOGOUT);
      this.$router.push('/login');
    },
    initObject(obj) {
      Object.keys(obj).forEach((index) => {
        obj[index] = null;
      });
      return obj;
    },
    initBikeForm() {
      this.bike_form_dict = this.initObject(this.bike_form_dict);
      if (typeof this.$refs.validation_bike_form !== 'undefined') {
        this.$refs.validation_bike_form.resetValidation();
      }
      this.bike_form_dict.setup_individual =
        [this.initObject(_.clone(this.setup_individual_dict, true))];
      this.edit = false;
    },
    initTrainingForm() {
      this.training_form_dict = this.initObject(this.training_form_dict);
      this.training_form_dict.setup_fixed =
        [this.initObject(_.clone(this.setup_fixed_dict, true))];
      this.training_form_dict.setup_individual =
        [this.bike_list[this.selected_bike.index].setup];
      for (let i = 0; i < Object.values(this.training_form_dict.setup_individual[0]).length; i += 1) {
        this.training_form_dict.setup_individual[0][i] = Object.assign(
          this.training_form_dict.setup_individual[0][i],
          { 'ticks_current': _.clone(
              this.training_form_dict.setup_individual[0][i].ticks_standard)
          }
        )
      }
    },
    addTab() {
      this.training_form_dict.setup_fixed
        .push(this.initObject(_.clone(this.setup_fixed_dict, true)));
      this.training_setup_tabs += 1;
      this.$nextTick(() => {
        this.training_setup_tab = this.training_setup_tabs;
      });
    },
    addSetupRow() {
      this.bike_form_dict.setup_individual
        .push(this.initObject(this.setup_individual_dict, true));
      this.setup_entries += 1;
    }
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
