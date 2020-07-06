<template>
  <div>
    <v-list-item @click="editTraining">
      <v-list-item-icon>
        <v-icon>mdi-dumbbell</v-icon>
      </v-list-item-icon>
      <v-list-item-title>
        Training
      </v-list-item-title>
    </v-list-item>
    <TrainingDialog
      :setup-fixed-template="setup_fixed_template"
      :setup-individual-template="setup_individual_template"
      :training-form-object="training_form_object"
      @updatedBike="updatedBike()"
      @cancelClicked="initTrainingForm()"
    />
  </div>
</template>

<script>
import {
  indexOfObjectValueInArray,
  initObject,
} from '../../utils/FromUtils';
import TrainingDialog from './TrainingDialog.vue';

export default {
  name: 'TheNavigationDrawerTraining',
  components: {
    TrainingDialog,
  },
  props: {
    bikeArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    training_form_object: {
      race_track: null,
      date: null,
      setup_fixed: [
        {
          operating_hours: null,
          slick_pressure_front: null,
          slick_pressure_rear: null,
          rain_pressure_front: null,
          rain_pressure_rear: null,
        },
      ],
      setup_individual: null,
    },
    setup_fixed_template: {
      operating_hours: null,
      slick_pressure_front: null,
      slick_pressure_rear: null,
      rain_pressure_front: null,
      rain_pressure_rear: null,
    },
    setup_individual_template: [],
  }),
  updated() {
  },
  created() {
  },
  methods: {
    updatedBike() {
      this.$emit('updatedBike');
    },
    editTraining() {
      this.$store.commit('setTrainingDialogState', true);
      this.initTrainingForm();
    },
    initTrainingForm() {
      const bikeIndex = indexOfObjectValueInArray(
        this.bikeArray, this.$store.getters.getCurrentBikeId,
      );
      initObject(this.training_form_object, null);
      this.training_form_object.date = new Date().toISOString().substr(0, 10);
      this.training_form_object.setup_fixed = [this._.cloneDeep(this.setup_fixed_template)];
      this.training_form_object.setup_fixed[0].operating_hours = this
        .$store.getters.getCurrentBikeOperatingHours;
      if (this.bikeArray[bikeIndex].setup != null) {
        this.training_form_object.setup_individual = [
          this._.cloneDeep(this.bikeArray[bikeIndex].setup),
        ];
        // eslint-disable-next-line prefer-destructuring
        this.setup_individual_template = this.training_form_object.setup_individual[0];
      } else {
        this.training_form_object.setup_individual = [];
      }
      this.$store.commit('setTrainingDialogSetupPanel', 0);
      this.$store.commit('setTrainingDialogSetupTabs', 1);
      this.$store.commit('setTrainingDialogSetupActiveTab', 0);
    },
  },
};
</script>

<style scoped>

</style>
