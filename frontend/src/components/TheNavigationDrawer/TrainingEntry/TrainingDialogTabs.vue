<template>
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
                      "training_form_object.setup_fixed
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
                          "training_form_object.setup_fixed
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
                          "training_form_object.setup_fixed
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
                          "training_form_object.setup_fixed
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
                          "training_form_object.setup_fixed
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
                     v-for="(setup_entry, setup_index) in training_form_object
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
</template>

<script>
import {FormUtils} from "../../utils/FromUtils";

export default {
  name: 'TheNavigationDrawerTrainingDialogTabs',
  props: {
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    training_setup_panel: 0,
    training_setup_tabs: 1,
    training_setup_tab: null,
    engine_mode: null,
    rain_tires: 0,
  }),
  methods: {
    incrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.incrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1)
    },
    decrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.decrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1)
    },
    incrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_front =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_front, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_front =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_front, 0.1, 1)
      }
    },
    decrementTirePressureFront(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_front =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_front, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_front =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_front, 0.1, 1)
      }
    },
    incrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_rear =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_rear, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_rear =
          FormUtils.incrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_rear, 0.1, 1)
      }
    },
    decrementTirePressureRear(ind) {
      if (this.rain_tires === 0) {
        this.training_form_object.setup_fixed[ind].slick_pressure_rear =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].slick_pressure_rear, 0.1, 1)
      } else {
        this.training_form_object.setup_fixed[ind].rain_pressure_rear =
          FormUtils.decrementNumber(
            this.training_form_object.setup_fixed[ind].rain_pressure_rear, 0.1, 1)
      }
    },
    incrementSetup(tabIndex, setupIndex) {
      this.training_form_object.setup_individual[tabIndex][setupIndex].ticks_current += 1;
      this.$forceUpdate();
    },
    decrementSetup(tabIndex, setupIndex) {
      this.training_form_object.setup_individual[tabIndex][setupIndex].ticks_current -= 1;
      this.$forceUpdate();
    },
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
    addTab() {
      this.training_form_object.setup_fixed
        .push(this.initObject(_.clone(this.setup_fixed_dict, true)));
      this.training_setup_tabs += 1;
      this.$nextTick(() => {
        this.training_setup_tab = this.training_setup_tabs;
      });
    },
  }
}
</script>

<style scoped>

</style>
