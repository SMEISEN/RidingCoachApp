<template>
  <v-card-text>
    <v-expansion-panels
      v-model="training_general_panel"
      focusable
    >
      <TrainingDialogGeneralLocation
        :training-form-object="trainingFormObject"
      />
      <TrainingDialogGeneralWeather
        :training-form-object="trainingFormObject"
      />
    </v-expansion-panels>
  </v-card-text>
</template>

<script>
import TrainingDialogGeneralLocation from './TrainingDialogGeneralLocation.vue';
import TrainingDialogGeneralWeather from './TrainingDialogGeneralWeather.vue';

export default {
  name: 'TrainingDialogGeneral',
  components: {
    TrainingDialogGeneralLocation,
    TrainingDialogGeneralWeather,
  },
  props: {
    trainingFormObject: {
      type: Object,
      required: true,
    },
    validTrainingDialog: {
      type: Boolean,
      required: true,
    },
  },
  data: () => ({
    training_general_panel: 0,
    location_object: {},
    weather_array: [],
  }),
  updated() {
  },
  created() {
  },
};
</script>

<style scoped>

</style>
