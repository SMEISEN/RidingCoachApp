<template>
  <div>
    <v-tabs
      v-model="training_setup_tab"
      background-color="secondary"
      dark
    >
      <v-tab
        v-for="training_tab_index in training_setup_tabs"
        :key="'tab/' + training_tab_index"
        @click="$forceUpdate()"
      >
        Setup {{ training_tab_index }}
      </v-tab>
      <v-tab-item
        v-for="training_tab_item_index in training_setup_tabs"
        :key="'tab-item/' + training_tab_item_index"
      >
        <v-card class="px-2">
          <v-btn
            fab
            absolute
            top
            right
            x-small
            color="error"
            @click.prevent="onSetupDelete()"
          >
            <v-icon dark>
              mdi-delete
            </v-icon>
          </v-btn>
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
                  v-model="trainingFormObject.setup_fixed[training_setup_tab].comment"
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
                  v-model="time_menu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  scrollable
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="trainingFormObject.setup_fixed[training_setup_tab].time"
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
                    v-model="trainingFormObject.setup_fixed[training_setup_tab].time"
                    format="24hr"
                    scrollable
                    full-width
                    @click:minute="time_menu = false"
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
            :tab-item-index="training_tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsTires
            :tab-item-index="training_tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsSetup
            :tab-item-index="training_tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
          <TrainingDialogTabsElectronic
            :tab-item-index="training_tab_item_index-1"
            :training-form-object="trainingFormObject"
          />
        </v-expansion-panels>
      </v-tab-item>
      <v-btn
        depressed
        height="47px"
        color="secondary"
        @click.prevent="addSetupTab()"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-tabs>
    <v-card
      v-if="trainingFormObject.sessions.length > 0"
      color="secondary"
      dark
    >
      <v-card-title
        style="height: 50px"
        class="pl-4 py-0 pr-2"
        @click="training_session_panel = !training_session_panel"
      >
        <span
          style="font-size: 16px"
        >
          Laptimes
        </span>
        <v-spacer />
        <v-avatar
          icon
        >
          <v-icon>{{ training_session_panel ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-avatar>
      </v-card-title>
      <v-expand-transition>
        <div v-show="training_session_panel">
          <v-tabs
            v-model="training_session_tab"
            background-color="secondary"
            dark
            vertical
          >
            <v-tab
              v-for="session_tab_index in training_session_tabs"
              :key="'tab/' + session_tab_index"
              @click="$forceUpdate()"
            >
              Session {{ session_tab_index }}
            </v-tab>
            <v-tab-item
              v-for="session_tab_item_index in training_session_tabs"
              :key="'tab-item/' + session_tab_item_index"
            >
              <TrainingDialogTabsLaptimes
                :session-object="trainingFormObject.sessions[session_tab_item_index-1]"
              />
            </v-tab-item>
          </v-tabs>
        </div>
      </v-expand-transition>
    </v-card>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'setup entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
    <InfoDialog
      :info-dialog.sync="info_dialog"
      :info-text="'The initial setup of a training can not be deleted!'"
    />
  </div>
</template>

<script>
import TrainingDialogTabsEngine from './TrainingDialogTabsEngine.vue';
import TrainingDialogTabsTires from './TrainingDialogTabsTires.vue';
import TrainingDialogTabsSetup from './TrainingDialogTabsSetup.vue';
import TrainingDialogTabsElectronic from './TrainingDialogTabsElectronic.vue';
import TrainingDialogTabsLaptimes from './TrainingDialogTabsLaptimes.vue';
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';
import InfoDialog from '../../common/InfoDialog.vue';
import { apiDeleteSetupItem } from '../../api/SetupApi';

export default {
  name: 'TrainingDialogTabs',
  components: {
    InfoDialog,
    ConfirmDeleteDialog,
    TrainingDialogTabsElectronic,
    TrainingDialogTabsSetup,
    TrainingDialogTabsTires,
    TrainingDialogTabsEngine,
    TrainingDialogTabsLaptimes,
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
    confirm_delete_dialog: false,
    info_dialog: false,
    new_tabs: [],
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
    training_session_tabs: {
      get() {
        return this.$store.getters.getTrainingDialogSessionTabs;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSessionTabs', value);
      },
    },
    training_session_tab: {
      get() {
        return this.$store.getters.getTrainingDialogSessionActiveTab;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSessionActiveTab', value);
      },
    },
    training_session_panel: {
      get() {
        return this.$store.getters.getTrainingDialogSessionPanel;
      },
      set(value) {
        this.$store.commit('setTrainingDialogSessionPanel', value);
      },
    },
    training_dialog() {
      return this.$store.getters.getTrainingDialogState;
    },
  },
  methods: {
    addSetupTab() {
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
        this.training_setup_tab = this.training_setup_tabs - 1;
      });
    },
    refreshTime() {
      this.trainingFormObject.setup_fixed[this.training_setup_tab].time = new Date()
        .toTimeString().substr(0, 5);
      this.$forceUpdate();
    },
    onSetupDelete() {
      const currentTab = this.training_setup_tab;
      if (currentTab !== 0) {
        this.confirm_delete_dialog = true;
      } else {
        this.info_dialog = true;
      }
    },
    deletionConfirmed() {
      const currentTab = this.training_setup_tab;
      const setupId = this.trainingFormObject.setup_fixed[currentTab].setup_id;
      this.trainingFormObject.setup_fixed.splice(currentTab, 1);
      this.trainingFormObject.setup_individual.splice(currentTab, 1);
      this.training_setup_tab -= 1;
      this.training_setup_tabs -= 1;
      if (setupId !== null) {
        apiDeleteSetupItem(setupId)
          .then(() => {
            this.$emit('deletionConfirmed', this.history_id);
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: 'Setup entry deleted!',
            });
          })
          .catch((error) => {
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
          });
      }
    },
  },
};
</script>
