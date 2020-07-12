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
      <v-card class="px-2">
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="9"
              md="10"
              class="px-6"
            >
              <v-textarea
                v-model="trainingFormObject.setup_fixed[training_setup_no].comment"
                label="Comment"
                rows="1"
                auto-grow
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="3"
              md="2"
              class="px-6"
            >
              <v-menu
                ref="time_menu"
                :v-model="time_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="trainingFormObject.setup_fixed[training_setup_no].time"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="trainingFormObject.setup_fixed[training_setup_no].time"
                    prepend-icon="mdi-clock"
                    append-outer-icon="mdi-update"
                    :rules="[v => !!v]"
                    readonly
                    required
                    @click:append-outer.prevent="refreshTime"
                    v-on="on"
                  />
                </template>
                <v-time-picker
                  v-if="time_menu"
                  v-model="trainingFormObject.setup_fixed[training_setup_no].time"
                  format="24hr"
                  scrollable
                  full-width
                  @click:minute="$refs.time_menu
                    .save(trainingFormObject.setup_fixed[training_setup_no].time)"
                />
              </v-menu>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-expansion-panels
        v-model="training_setup_panel"
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
  data: () => ({
    time_menu: false,
  }),
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
    training_setup_no() {
      if (this.training_setup_tab === 0) {
        return 0;
      }
      return this.training_setup_tab - 1;
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
      this.trainingFormObject.setup_fixed[numberOfTabs + 1].setup_id = null;
      this.trainingFormObject.setup_fixed[numberOfTabs + 1].time = new Date()
        .toTimeString().substr(0, 5);
      this.trainingFormObject.setup_individual
        .push(this._.cloneDeep(this.trainingFormObject.setup_individual[numberOfTabs]));
      this.training_setup_tabs += 1;
      this.$nextTick(() => {
        this.training_setup_tab = this.training_setup_tabs;
      });
    },
    refreshTime() {
      this.trainingFormObject.setup_fixed[this.training_setup_no].time = new Date()
        .toTimeString().substr(0, 5);
      this.$forceUpdate();
    },
  },
};
</script>

<style scoped>

</style>
