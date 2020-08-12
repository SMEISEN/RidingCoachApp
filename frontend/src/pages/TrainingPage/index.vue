<template>
  <v-app>
    <v-card
      :height="0.88 * window_height"
      style="overflow-y:auto;"
    >
      <v-card-title class="pa-0">
        <v-toolbar app top short flat>
          <v-btn-toggle
            v-model="timeline_buttons"
            mandatory
            dense
            style="width:100%"
          >
            <v-menu
              ref="menu"
              v-model="date_menu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  style="min-width:20%"
                  x-small
                  v-bind="attrs"
                  v-on="on"
                >
                  {{ displayed_date }}
                </v-btn>
              </template>
              <v-date-picker
                v-model="picked_date"
                type="month"
                scrollable
                no-title
                @input="date_menu = false"
              >
              </v-date-picker>
            </v-menu>
            <v-btn
              style="min-width:20%"
              x-small
            >
              {{ new Date().getFullYear() }}
            </v-btn>
            <v-btn
              style="min-width:20%"
              x-small
            >
              {{ new Date(new Date().setMonth(new Date().getMonth() - 1))
                .toLocaleString('en-US', { month: 'short' }) }}
            </v-btn>
            <v-btn
              style="min-width:20%"
              x-small
            >
              {{ new Date().toLocaleString('en-US', { month: 'short' }) }}
            </v-btn>
            <v-btn
              style="min-width:20%"
              x-small
            >
              now
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
      </v-card-title>
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
    </v-card>
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
    timeline_buttons: 4,
    show_training: false,
    training_array: null,
    date_menu: false,
    picked_date: null,
    window_height: null,
  }),
  computed: {
    displayed_date() {
      if (this.timeline_buttons !== 0) {
        return 'pick';
      } if (this.picked_date === null) {
        return new Date().toLocaleString('en-US',
          {
            year: '2-digit',
            month: 'short',
          });
      }
      const pickedDate = new Date(this.picked_date);
      return `${
        pickedDate.toLocaleString('en-US', { month: 'short' })} ${
        pickedDate.toLocaleString('en-US', { year: '2-digit' })}`;
    },
  },
  updated() {
    this.window_height = window.innerHeight;
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
