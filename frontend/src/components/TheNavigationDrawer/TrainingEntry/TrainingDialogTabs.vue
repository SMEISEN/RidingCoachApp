<template>
  <v-tabs
    v-model="training_setup_tab"
    background-color="secondary"
    dark
  >
    <v-tab
      v-for="tab_index in training_setup_tabs"
      :key="'tab/' + tab_index"
      @click="$forceUpdate()"
    >
      Setup {{ tab_index }}
    </v-tab>
    <v-tab-item
      v-for="tab_item_index in training_setup_tabs"
      :key="'tab-item/' + tab_item_index"
    >
      <v-card-text>
        <v-expansion-panels
          popout
          focusable
          v-model="training_setup_panel"
        >
          <TrainingDialogTabsEngine
            :tab_item_index="tab_item_index-1"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsTires
            :tab_item_index="tab_item_index-1"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsSetup
            :tab_item_index="tab_item_index-1"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsElectronic
            :tab_item_index="tab_item_index-1"
            :training_form_object="training_form_object"
          />
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
import TrainingDialogTabsEngine from './TrainingDialogTabsEngine';
import TrainingDialogTabsTires from './TrainingDialogTabsTires';
import TrainingDialogTabsSetup from './TrainingDialogTabsSetup';
import TrainingDialogTabsElectronic from './TrainingDialogTabsElectronic';
import _ from 'lodash';

export default {
  name: 'TheNavigationDrawerTrainingDialogTabs',
  components: {
    TrainingDialogTabsElectronic,
    TrainingDialogTabsSetup,
    TrainingDialogTabsTires,
    TrainingDialogTabsEngine},
  props: {
    setup_fixed_template: {
      type: Object,
      required: true,
    },
    setup_individual_template: {
      type: Array,
      required: true,
    },
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  computed: {
    training_setup_panel: {
      get() {
        return this.$store.getters.getTrainingDialogSetupPanel;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSetupPanel', value);
      },
    },
    training_setup_tabs: {
      get() {
        return this.$store.getters.getTrainingDialogSetupTabs;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSetupTabs', value);
      },
    },
    training_setup_tab: {
      get() {
        return this.$store.getters.getTrainingDialogSetupActiveTab;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSetupActiveTab', value);
      },
    },
  },
  methods: {
    addTab() {
      const number_of_tabs = this.training_form_object.setup_fixed.length - 1;
      this.training_form_object.setup_fixed
        .push(_.cloneDeep(this.training_form_object.setup_fixed[number_of_tabs]));
      this.training_form_object.setup_individual
        .push(_.cloneDeep(this.training_form_object.setup_individual[number_of_tabs]));
      this.training_setup_tabs += 1;
      this.$nextTick(() => {
        this.training_setup_tab = this.training_setup_tabs;
      });
    },
  },
  updated() {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
