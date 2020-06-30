<template>
  <v-tabs
    v-model="training_setup_tab"
    background-color="secondary"
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
          v-model="training_setup_panel"
          popout
          focusable
        >
          <TrainingDialogTabsEngine
            :tab-item-index="tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsTires
            :tab-item-index="tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsSetup
            :tab-item-index="tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsElectronic
            :tab-item-index="tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
        </v-expansion-panels>
      </v-card-text>
    </v-tab-item>
    <v-tab @click="addTab">
      <v-icon>mdi-plus</v-icon>
    </v-tab>
    <v-tab-item />
  </v-tabs>
</template>

<script>
import TrainingDialogTabsEngine from './TrainingDialogTabsEngine.vue';
import TrainingDialogTabsTires from './TrainingDialogTabsTires.vue';
import TrainingDialogTabsSetup from './TrainingDialogTabsSetup.vue';
import TrainingDialogTabsElectronic from './TrainingDialogTabsElectronic.vue';

export default {
  name: 'TrainingDialogTabs',
  components: {
    TrainingDialogTabsElectronic,
    TrainingDialogTabsSetup,
    TrainingDialogTabsTires,
    TrainingDialogTabsEngine,
  },
  props: {
    setupFixedTemplate: {
      type: Object,
      required: true,
    },
    setupIndividualTemplate: {
      type: Array,
      required: true,
    },
    trainingFormObject: {
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
  updated() {
  },
  created() {
  },
  methods: {
    addTab() {
      const numberOfTabs = this.trainingFormObject.setup_fixed.length - 1;
      this.trainingFormObject.setup_fixed
        .push(this._.cloneDeep(this.trainingFormObject.setup_fixed[numberOfTabs]));
      this.trainingFormObject.setup_individual
        .push(this._.cloneDeep(this.trainingFormObject.setup_individual[numberOfTabs]));
      this.training_setup_tabs += 1;
      this.$nextTick(() => {
        this.training_setup_tab = this.training_setup_tabs;
      });
    },
  },
};
</script>

<style scoped>

</style>
