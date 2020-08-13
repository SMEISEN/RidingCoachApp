<template>
  <v-app>
    <v-card
      :height="0.88 * window_height"
      style="overflow-y:auto;"
    >
      <v-card-title class="pa-0">
        <TimelineToolbar
          :timeline-buttons.sync="timeline_buttons"
          :picked-date.sync="picked_date"
        />
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
import TimelineToolbar from './TimelineToolbar.vue';
import { apiQueryTrainings } from '../../components/api/TrainingApi';
import { indexOfObjectValueInArray } from '../../components/utils/FromUtils';

export default {
  name: 'Training',
  metaInfo: {
    title: 'Training',
  },
  components: {
    TimelineToolbar,
    TimelineCard,
  },
  data: () => ({
    timeline_buttons: 4,
    show_training: false,
    training_array: null,
    window_height: null,
    picked_date: new Date().toISOString().substr(0, 7),
  }),
  watch: {
    timeline_buttons() {
      if (this.timeline_buttons === 4) {
        this.getDateNow();
      } if (this.timeline_buttons === 3) {
        this.getDateThisMonth();
      } if (this.timeline_buttons === 2) {
        this.getDateLastMonth();
      } if (this.timeline_buttons === 1) {
        this.getDateThisYear();
      }
    },
    picked_date() {
      if (this.timeline_buttons === 0) {
        const year = new Date(this.picked_date).getFullYear();
        const monthStart = new Date(this.picked_date).getMonth();
        const monthEnd = new Date(this.picked_date).getMonth() + 1;
        const dateStart = new Date(
          new Date(this.picked_date).setUTCHours(0, 0, 0, 0),
        ).setUTCFullYear(year, monthStart, 1) / 1000;
        const dateEnd = new Date(
          new Date(this.picked_date).setUTCHours(0, 0, 0, 0),
        ).setUTCFullYear(year, monthEnd, 0) / 1000;
        const query = {
          datetime_display: {
            values: [Math.round(dateStart), Math.round(dateEnd)],
            operators: ['>=', '<='],
          },
        };
        this.queryTrainings(query);
      }
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
    this.getDateNow();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setTrainingDialogState'
        && this.$store.getters.getTrainingDialogState === false) {
        this.getDateNow();
      }
    });
  },
  methods: {
    queryTrainings(query) {
      apiQueryTrainings(query).then((res) => {
        this.training_array = res.data;
      });
    },
    removeTraining(trainingId) {
      const trainingIndex = indexOfObjectValueInArray(this.training_array, trainingId);
      this.training_array.splice(trainingIndex, 1);
    },
    getDateNow() {
      const dateValue = new Date()
        .setUTCHours(0, 0, 0, 0) / 1000 - 30 * 24 * 60 * 60;
      const query = {
        datetime_display: {
          values: [Math.round(dateValue)],
          operators: ['>='],
        },
      };
      this.queryTrainings(query);
    },
    getDateThisMonth() {
      const year = new Date().getFullYear();
      const monthStart = new Date().getMonth();
      const monthEnd = new Date().getMonth() + 1;
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      const query = {
        datetime_display: {
          values: [Math.round(dateStart), Math.round(dateEnd)],
          operators: ['>=', '<='],
        },
      };
      this.queryTrainings(query);
    },
    getDateLastMonth() {
      const year = new Date().getFullYear();
      const monthStart = new Date().getMonth() - 1;
      const monthEnd = new Date().getMonth();
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      const query = {
        datetime_display: {
          values: [Math.round(dateStart), Math.round(dateEnd)],
          operators: ['>=', '<='],
        },
      };
      this.queryTrainings(query);
    },
    getDateThisYear() {
      const year = new Date().getFullYear();
      const monthStart = 0;
      const monthEnd = new Date().getMonth() + 1;
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      const query = {
        datetime_display: {
          values: [Math.round(dateStart), Math.round(dateEnd)],
          operators: ['>=', '<='],
        },
      };
      this.queryTrainings(query);
    },
  },
};
</script>

<style scoped>

</style>
