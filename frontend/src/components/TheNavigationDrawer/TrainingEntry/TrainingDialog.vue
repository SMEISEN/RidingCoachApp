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
</template>

<script>
import TrainingDialogTabs from './TrainingDialogTabs.vue';
import TrainingDialogGeneral from './TrainingDialogGeneral.vue';
import { apiGetBike, apiPutBike } from '../../api/BikeApi';

export default {
  name: 'TrainingDialog',
  components: {
    TrainingDialogTabs,
    TrainingDialogGeneral,
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
