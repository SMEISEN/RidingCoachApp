<template>
  <v-expansion-panels
    v-model="training_general_panel"
    focusable
  >
    <TrainingDialogGeneralLocation
      :training-form-object="trainingFormObject"
    />
    <TrainingDialogGeneralWeather
      v-if="$store.getters.getTrainingEditId === null"
      :training-form-object="trainingFormObject"
    />
  </v-expansion-panels>
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
};
</script>
