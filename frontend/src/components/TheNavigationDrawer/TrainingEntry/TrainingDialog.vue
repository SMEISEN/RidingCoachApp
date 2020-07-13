<template>
  <div>
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
                :disabled="!training_saved"
                @click.prevent="onTrainingDelete()"
              >
                Delete
              </v-btn>
              <v-btn
                text
                :disabled="!valid_training_dialog"
                @click.prevent="onTrainingSave()"
              >
                Save
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <TrainingDialogGeneral
            :training-form-object="trainingFormObject"
            :valid-training-dialog.sync="valid_training_dialog"
          />
          <TrainingDialogTabs
            :setup-fixed-template="setupFixedTemplate"
            :setup-individual-template="setupIndividualTemplate"
            :training-form-object="trainingFormObject"
          />
        </v-card>
      </v-form>
    </v-dialog>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'training entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deleteTrainingData()"
    />
  </div>
</template>

<script>
import TrainingDialogTabs from './TrainingDialogTabs.vue';
import TrainingDialogGeneral from './TrainingDialogGeneral.vue';
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';
import { apiPutBike } from '../../api/BikeApi';
import { apiDeleteTrainingItem, apiPostTraining, apiPutTrainingItem } from '../../api/TrainingApi';
import { apiDeleteSetupItem, apiPostSetup, apiPutSetupItem } from '../../api/SetupApi';

export default {
  name: 'TrainingDialog',
  components: {
    TrainingDialogTabs,
    TrainingDialogGeneral,
    ConfirmDeleteDialog,
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
    valid_training_dialog: true,
    confirm_delete_dialog: false,
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
    training_saved() {
      return this.trainingFormObject.training_id !== null;
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
      const bikeId = this.$store.getters.getCurrentBikeId;
      const payloadBike = {
        operating_hours: Math.max.apply(null,
          this._.map(this.trainingFormObject.setup_fixed, 'operating_hours')),
      };
      apiPutBike(bikeId, payloadBike).then(() => {
        this.$store.commit('setOperatingHours', payloadBike.operating_hours);
        this.updatedBike();
      });
      const datetime = this.trainingFormObject.date
        .concat('T', new Date().toTimeString().substr(0, 5));
      const payloadTraining = {
        location: this.trainingFormObject.race_track,
        weather_hourly: this.trainingFormObject.weather,
        datetime_display: Date.parse(datetime) / 1000,
      };
      if (this.trainingFormObject.training_id === null) {
        apiPostTraining(payloadTraining).then((resTraining) => {
          this.trainingFormObject.training_id = resTraining.data;
          for (let i = 0; i < this.trainingFormObject.setup_fixed.length; i += 1) {
            const payloadSetup = this.setupPayload(resTraining.data, i, bikeId);
            apiPostSetup(payloadSetup).then((resSetup) => {
              this.trainingFormObject.setup_fixed[i].setup_id = resSetup.data;
            });
          }
        });
      } else {
        const trainingId = this.trainingFormObject.training_id;
        apiPutTrainingItem(payloadTraining, trainingId).then(() => {
          for (let i = 0; i < this.trainingFormObject.setup_fixed.length; i += 1) {
            const payloadSetup = this.setupPayload(trainingId, i, bikeId);
            const setupId = this.trainingFormObject.setup_fixed[i].setup_id;
            if (setupId === null) {
              apiPostSetup(payloadSetup).then((resSetup) => {
                this.trainingFormObject.setup_fixed[i].setup_id = resSetup.data;
              });
            } else {
              apiPutSetupItem(payloadSetup, setupId);
            }
          }
        });
      }
      this.training_dialog = false;
      this.$emit('saveClicked');
    },
    onTrainingCancel() {
      this.training_dialog = false;
      this.$refs.validation_training_form.resetValidation();
      this.$emit('cancelClicked');
    },
    onTrainingDelete() {
      this.confirm_delete_dialog = true;
    },
    deleteTrainingData() {
      for (let i = 0; i < this.trainingFormObject.setup_fixed.length; i += 1) {
        const setupId = this.trainingFormObject.setup_fixed[i].setup_id;
        if (setupId !== null) {
          apiDeleteSetupItem(setupId).then(() => {
            this.trainingFormObject.setup_fixed[i].setup_id = null;
          });
        }
      }
      const trainingId = this.trainingFormObject.training_id;
      apiDeleteTrainingItem(trainingId).then(() => {
        this.training_dialog = false;
        this.$refs.validation_training_form.resetValidation();
        this.$emit('deletionConfirmed');
      });
    },
    setupPayload(trainingId, setupNo, bikeId) {
      const datetime = this.trainingFormObject.date
        .concat('T', this.trainingFormObject.setup_fixed[setupNo].time);
      return {
        training_id: trainingId,
        bike_id: bikeId,
        weather_current: this.trainingFormObject.setup_fixed[setupNo].weather_current,
        comment: this.trainingFormObject.setup_fixed[setupNo].comment,
        datetime_display: Date.parse(datetime) / 1000,
        operating_hours: this.trainingFormObject.setup_fixed[setupNo].operating_hours,
        slick_pressure_front: this.trainingFormObject.setup_fixed[setupNo].slick_pressure_front,
        slick_pressure_rear: this.trainingFormObject.setup_fixed[setupNo].slick_pressure_rear,
        rain_pressure_front: this.trainingFormObject.setup_fixed[setupNo].rain_pressure_front,
        rain_pressure_rear: this.trainingFormObject.setup_fixed[setupNo].rain_pressure_rear,
        setup: this.trainingFormObject.setup_individual[setupNo],
      };
    },
  },
};
</script>

<style scoped>

</style>
