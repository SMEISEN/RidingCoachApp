<template>
  <v-dialog
    v-model="training_dialog"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-form
      ref="validation_training_form"
      v-model="valid_training_dialog"
    >
      <v-card>
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            @click.prevent="onTrainingCancel()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Training settings</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <v-btn
              text
              :disabled="!valid_training_dialog"
              @click.prevent="onTrainingSave()"
            >
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-card-text>
          <v-expansion-panels
            v-model="training_general_panel"
            focusable
          >
            <v-expansion-panel>
              <v-expansion-panel-header>Location</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-col
                    cols="12"
                    xs="12"
                    sm="9"
                    md="10"
                    class="px-6"
                  >
                    <v-combobox
                      v-model="trainingFormObject.race_track"
                      label="Race track*"
                      :rules="[v => !!v]"
                      required
                    />
                  </v-col>
                  <v-col
                    cols="auto"
                    xs="12"
                    sm="3"
                    md="2"
                    class="px-6"
                  >
                    <v-menu
                      v-model="date_menu"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      scrollable
                      transition="scale-transition"
                      offset-y
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on }">
                        <v-text-field
                          v-model="trainingFormObject.date"
                          prepend-icon="mdi-calendar"
                          required
                          v-on="on"
                        />
                      </template>
                      <v-date-picker
                        v-model="trainingFormObject.date"
                        @input="date_menu = false"
                      />
                    </v-menu>
                  </v-col>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-header>Weather</v-expansion-panel-header>
              <v-expansion-panel-content />
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
        <TrainingDialogTabs
          :setup-fixed-template="setupFixedTemplate"
          :setup-individual-template="setupIndividualTemplate"
          :training-form-object="trainingFormObject"
        />
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import TrainingDialogTabs from './TrainingDialogTabs.vue';
import { apiGetBike, apiPutBike } from '../../api/BikeApi';

export default {
  name: 'TrainingDialog',
  components: {
    TrainingDialogTabs,
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
    date_menu: false,
    training_general_panel: 0,
    valid_training_dialog: true,
  }),
  computed: {
    training_dialog: {
      get() {
        return this.$store.getters.getTrainingDialogState;
      },
      set(value) {
        this.$store.commit('setTrainingDialogState', value);
      },
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    updatedBike() {
      this.$emit('updatedBike');
    },
    onTrainingSave() {
      const BikeId = this.$store.getters.getCurrentBikeId;
      apiGetBike(BikeId).then((res) => {
        const payload = res.data;
        payload.operating_hours = Math.max.apply(null,
          this._.map(this.trainingFormObject.setup_fixed, 'operating_hours'));
        apiPutBike(BikeId, payload).then(() => {
          this.$store.commit('setOperatingHours', payload.operating_hours);
          this.updatedBike();
        });
        this.training_dialog = false;
        this.$emit('saveClicked');
      });
    },
    onTrainingCancel() {
      this.training_dialog = false;
      this.training_setup_tabs = 1;
      this.training_setup_tab = null;
      this.$emit('cancelClicked');
    },
  },
};
</script>

<style scoped>

</style>
