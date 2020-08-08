<template>
  <v-app>
    <v-container>
      <v-timeline
        dense
        clipped
        class="ml-n9"
      >
        <v-timeline-item
          v-for="training_item in training_array"
          :key="'training/' + training_item.training_id"
          color="primary"
          small
        >
          <TimelineCard
            :training-item="training_item"
            @removedTraining="removeTraining"
          />
        </v-timeline-item>
      </v-timeline>
    </v-container>
  </v-app>
</template>

<script>
import TimelineCard from './TimelineCard.vue';
import { apiGetTrainings } from '../../components/api/TrainingApi';
import { indexOfObjectValueInArray } from '../../components/utils/FromUtils';

export default {
  name: 'Training',
  metaInfo: {
    title: 'Training',
  },
  components: {
    TimelineCard,
  },
  data: () => ({
    show_training: false,
    training_array: null,
  }),
  updated() {
  },
  created() {
    this.getTrainings();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setTrainingDialogState'
        && this.$store.getters.getTrainingDialogState === false) {
        this.getTrainings();
      }
    });
  },
  methods: {
    getTrainings() {
      apiGetTrainings().then((res) => {
        this.training_array = res.data;
      });
    },
    removeTraining(trainingId) {
      const trainingIndex = indexOfObjectValueInArray(this.training_array, trainingId);
      this.training_array.splice(trainingIndex, 1);
    },
  },
};
</script>

<style scoped>

</style>
