<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Engine</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-container>
        <div
          v-for="(setup_group, group_index) in setup_groups"
          :key="'tab-item/' + tabItemIndex + '/setup-group/' + group_index"
        >
          <v-row
            dense
            align="start"
          >
            <v-col
              v-if="group_index === 0"
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-subheader>Operating hours*</v-subheader>
              <v-text-field
                v-model="trainingFormObject.setup_fixed[tabItemIndex].operating_hours"
                dense
                :rules="[v => !!v]"
                required
                suffix="h"
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer="incrementHour(tabItemIndex)"
                @click:prepend="decrementHour(tabItemIndex)"
              />
            </v-col>
            <v-col
              v-for="(setup_entry, setup_index) in setupByGroup(setup_group)"
              :key="'tab-item/' + tabItemIndex + '/setup-group/' + group_index
                + '/setup-item/' + setup_index"
              cols="12"
              xs="12"
              sm="6"
              md="6"
              class="px-16"
            >
              <v-subheader v-if="setup_group === null">
                {{ setup_entry.name }}
              </v-subheader>
              <v-subheader v-else>
                {{ setup_group + ' ' + setup_entry.name }}
              </v-subheader>
              <hr style="height:3pt; visibility:hidden;">
              <TrainingDialogTabsSlider
                :setup-entry="setup_entry"
              />
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import {
  incrementNumber,
  decrementNumber,
} from '../../utils/FromUtils';
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider.vue';

export default {
  name: 'TrainingDialogTabsEngine',
  components: {
    TrainingDialogTabsSlider,
  },
  props: {
    tabItemIndex: {
      type: Number,
      required: true,
    },
    trainingFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    setup_groups: [null],
  }),
  computed: {
    engine_setup() {
      if (this.trainingFormObject.setup_individual.length > 0) {
        return this.trainingFormObject.setup_individual[this.tabItemIndex]
          .filter((i) => i.category === 'Engine');
      }
      return this.trainingFormObject.setup_individual;
    },
  },
  updated() {
  },
  created() {
    this.getSetupGroups();
  },
  methods: {
    incrementHour(ind) {
      this.trainingFormObject.setup_fixed[ind].operating_hours = incrementNumber(
        this.trainingFormObject.setup_fixed[ind].operating_hours, 0.1, 1,
      );
    },
    decrementHour(ind) {
      this.trainingFormObject.setup_fixed[ind].operating_hours = decrementNumber(
        this.trainingFormObject.setup_fixed[ind].operating_hours, 0.1, 1,
      );
    },
    setupByGroup(group) {
      return this.engine_setup.filter((i) => i.group === group);
    },
    getSetupGroups() {
      this.setup_groups = this._.uniq(
        Object.assign(this.setup_groups,
          Object.values(
            this._.mapValues(
              this.engine_setup, 'group',
            ),
          )),
      );
    },
  },
};
</script>

<style scoped>

</style>
