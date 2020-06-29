<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Electronic</v-expansion-panel-header>
    <v-expansion-panel-content>
      <div v-for="(setup_group, group_index) in setup_groups"
           :key="'tab-item/' + tab_item_index + '/setup-group/' + group_index">
        <v-row dense>
          <v-col cols="12" xs="12" sm="3" md="3" class="px-6"
                 v-for="(setup_entry, setup_index) in setupByGroup(setup_group)"
                 :key="'tab-item/' + tab_item_index + '/setup-group/' + group_index
                 + '/setup-item/' + setup_index"
          >
            <v-subheader v-if="setup_entry.group === ''">{{ setup_entry.name }}</v-subheader>
            <v-subheader v-else>{{ setup_entry.group + ' ' + setup_entry.name }}</v-subheader>
            <TrainingDialogTabsSlider
              :setup_entry="setup_entry"
            />
          </v-col>
        </v-row>
        <v-divider v-if="group_index !== Object.keys(setup_groups).length - 1"/>
      </div>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider';
import _ from 'lodash';

export default {
  name: 'TrainingDialogTabsElectronic',
  components: {
    TrainingDialogTabsSlider,
  },
  props: {
    tab_item_index: {
      type: Number,
      required: true,
    },
    training_form_object: {
      type: Object,
      required:true,
    },
  },
  computed: {
    electronic_setup() {
      return this.training_form_object.setup_individual[this.tab_item_index]
        .filter(i => i.category === 'Electronic');
    },
  },
  data: () => ({
    setup_groups: null
  }),
  methods: {
    setupByGroup(group) {
      return this.electronic_setup.filter(i => i.group === group);
    },
    getSetupGroups() {
      this.setup_groups =
        _.uniq(
          Object.values(
            _.mapValues(
              this.suspension_setup, 'group'
            )
          )
        );
    },
  },
  updated() {
  },
  created() {
    this.getSetupGroups();
  },
}
</script>

<style scoped>

</style>
