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
          <TrainingDialogTabsEngine
            :tab_item_index="tab_item_index"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsTires
            :tab_item_index="tab_item_index"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsSetup
            :tab_item_index="tab_item_index"
            :training_form_object="training_form_object"
          />
          <TrainingDialogTabsElectronic
            :tab_item_index="tab_item_index"
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
import TrainingDialogTabsElectronic from "./TrainingDialogTabsElectronic";

export default {
  name: 'TheNavigationDrawerTrainingDialogTabs',
  components: {
    TrainingDialogTabsElectronic,
    TrainingDialogTabsSetup,
    TrainingDialogTabsTires,
    TrainingDialogTabsEngine},
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
  }),
  methods: {
    addTab() {
      this.training_form_object.setup_fixed
        .push(this.initObject(_.clone(this.setup_fixed_dict, true)));
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
