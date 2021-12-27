<template>
  <v-expansion-panel v-if="suspension_setup.length > 0">
    <v-expansion-panel-header>Suspension</v-expansion-panel-header>
    <v-expansion-panel-content>
      <div
        v-for="(setup_group, group_index) in setup_groups"
        :key="'tab-item/' + tabItemIndex + '/setup-group/' + group_index"
      >
        <v-row dense>
          <v-col
            v-for="(setup_entry, setup_index) in setupByGroup(setup_group)"
            :key="'tab-item/' + tabItemIndex + '/setup-group/' + group_index
              + '/setup-item/' + setup_index"
            cols="12"
            xs="12"
            sm="3"
            md="3"
            class="px-6"
          >
            <v-subheader v-if="setup_entry.group === ''">
              {{ setup_entry.name }}
            </v-subheader>
            <v-subheader v-else>
              {{ setup_entry.group + ' ' + setup_entry.name }}
            </v-subheader>
            <TrainingDialogTabsSlider
              :setup-entry="setup_entry"
            />
          </v-col>
        </v-row>
        <v-divider v-if="group_index !== Object.keys(setup_groups).length - 1" />
      </div>
      <br>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import TrainingDialogTabsSlider from './TrainingDialogTabsSlider.vue';

export default {
  name: 'TrainingDialogTabsSetup',
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
    setup_groups: [''],
  }),
  computed: {
    suspension_setup() {
      if (this.trainingFormObject.setup_individual.length > 0) {
        if (this.trainingFormObject.setup_individual[this.tabItemIndex].length > 0) {
          return this.trainingFormObject.setup_individual[this.tabItemIndex]
            .filter((i) => i.category === 'Suspension');
        }
      }
      return [];
    },
  },
  created() {
    this.getSetupGroups();
  },
  methods: {
    /**
     * Filters the suspension setup for the given setup group.
     * @param {string} group setup group
     * @returns {T[]}
     */
    setupByGroup(group) {
      return this.suspension_setup.filter((i) => i.group === group);
    },
    /**
     * Extracts the groups of the suspension setup.
     */
    getSetupGroups() {
      this.setup_groups = this._.uniq(
        Object.assign(this.setup_groups,
          Object.values(
            this._.mapValues(
              this.suspension_setup, 'group',
            ),
          )),
      );
    },
  },
};
</script>
