<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Engine</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-container>
        <div v-for="(setup_group, group_index) in setup_groups"
             :key="'tab-item/' + tab_item_index + '/setup-group/' + group_index">
          <v-row dense align="start">
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16"
                   v-if="setup_group === '' && group_index === 0">
              <v-subheader>Operating hours*</v-subheader>
              <v-text-field
                dense
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementHour(tab_item_index)"
                @click:prepend="decrementHour(tab_item_index)"
                :rules="[v => !!v]"
                required
                suffix="h"
                v-model="training_form_object.setup_fixed[tab_item_index].operating_hours">
              </v-text-field>
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="6" class="px-16"
                   v-for="(setup_entry, setup_index) in setupByGroup(setup_group)"
                   :key="'tab-item/' + tab_item_index + '/setup-group/' + group_index
                   + '/setup-item/' + setup_index">
              <v-subheader v-if="setup_group === ''">{{ setup_entry.name }}</v-subheader>
              <v-subheader v-else>{{ setup_group + ' ' + setup_entry.name }}</v-subheader>
              <hr style="height:3pt; visibility:hidden;" />
              <TrainingDialogTabsSlider
                :setup_entry="setup_entry"
              />
              <v-divider v-if="group_index !== Object.keys(setup_groups).length - 1"/>
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import {FormUtils} from '../../utils/FromUtils';
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider';

export default {
  name: 'TrainingDialogTabsEngine',
  components: {
    TrainingDialogTabsSlider,
  },
  props: {
    tab_item_index: {
      type: Number,
      required:true,
    },
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    setup_groups: null
  }),
  computed: {
    engine_setup() {
      return this.training_form_object.setup_individual[this.tab_item_index]
        .filter(i => i.category === 'Engine');
    },
  },
  methods: {
    incrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.incrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1);
    },
    decrementHour(ind) {
      this.training_form_object.setup_fixed[ind].operating_hours =
        FormUtils.decrementNumber(
          this.training_form_object.setup_fixed[ind].operating_hours, 0.1, 1);
    },
    setupByGroup(group) {
      return this.engine_setup.filter(i => i.group === group);
    },
    getSetupGroups() {
      this.setup_groups =
        _.uniq(
          Object.values(
            _.mapValues(
              this.engine_setup, 'group'
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
