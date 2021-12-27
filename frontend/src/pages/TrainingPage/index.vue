<template>
  <v-app>
    <v-card
      :height="0.88 * window_height"
      style="overflow-y:auto; overflow-x: hidden;"
    >
      <v-card-title class="pa-0">
        <TimelineToolbar
          :timeline-buttons.sync="timeline_buttons"
          :picked-date.sync="picked_date"
        />
      </v-card-title>
      <v-card-text>
        <v-timeline
          dense
          clipped
          class="ml-n9 mr-n4"
        >
          <div
            v-for="(month, index) in training_array_sorted"
            :key="'training/month' + index"
          >
            <v-timeline-item
              hide-dot
              class="ml-n6 mr-6"
            >
              <v-row>
                <v-col
                  cols="12"
                  class="text-right text-caption text--secondary"
                >
                  <v-divider />
                  {{ new Date(month[0].datetime_display)
                    .toLocaleString('en-US', { month: 'long' }) }}
                </v-col>
              </v-row>
            </v-timeline-item>
            <div
              v-for="(training_item) in month"
              :key="'training/month/' + index + '/item/' + training_item.training_id"
            >
              <v-timeline-item
                color="primary"
                small
              >
                <TimelineCard
                  :training-item="training_item"
                  @removedTraining="removeTraining"
                />
              </v-timeline-item>
            </div>
          </div>
        </v-timeline>
      </v-card-text>
      <v-row>
        <v-col
          cols="12"
          class="text-center"
        >
          <v-btn
            fab
            x-small
            color="accent"
            :loading="loading_trainings"
            @click="appendTraining()"
          >
            <v-icon>
              mdi-chevron-down
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
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
    training_array_sorted: null,
    weather_array_sorted: null,
    window_height: null,
    query: {},
    loading_trainings: false,
    picked_date: new Date().toISOString().substr(0, 7),
  }),
  computed: {
    current_bike_id() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  watch: {
    timeline_buttons() {
      this.loading_trainings = true;
      this.getTrainings();
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
        this.query.datetime_display = {
          values: [Math.round(dateStart), Math.round(dateEnd)],
          operators: ['>=', '<='],
        };
        this.queryTrainings();
      }
    },
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
    this.window_height = window.innerHeight;
    this.query.bike_id = this.current_bike_id;
    this.getTrainings();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setTrainingDialogState'
        && this.$store.getters.getTrainingDialogState === false) {
        this.getTrainings();
      }
      if (mutation.type === 'selectBike') {
        this.query.bike_id = this.current_bike_id;
        this.queryTrainings();
      }
    });
  },
  methods: {
    /**
     * Get trainings of the period selected in the toolbar menu.
     */
    getTrainings() {
      switch (this.timeline_buttons) {
        case 4:
          this.getDateNow();
          break;
        case 3:
          this.getDateThisMonth();
          break;
        case 2:
          this.getDateLastMonth();
          break;
        case 1:
          this.getDateThisYear();
          break;
        default:
          this.queryTrainings();
      }
    },
    /**
     * Query trainings from the database.
     */
    queryTrainings() {
      apiQueryTrainings(this.query).then((res) => {
        this.training_array = res.data;
        if (res.data.length > 0) {
          this.sortTrainingData(res.data);
        } else {
          this.training_array_sorted = [];
        }
        this.loading_trainings = false;
      });
    },
    /**
     * Removes a training from the display. Does not delete the training!
     * @param {string} trainingId id of the training
     */
    removeTraining(trainingId) {
      const trainingIndex = indexOfObjectValueInArray(this.training_array, trainingId);
      this.training_array.splice(trainingIndex, 1);
    },
    /**
     * Adds trainings to the display by adding 30 days to the considered period.
     */
    appendTraining() {
      this.timeline_buttons = 0;
      this.loading_trainings = true;
      const previousDate = this.query.datetime_display.values[0];
      this.query.datetime_display.values = [previousDate - 30 * 24 * 60 * 60];
      this.query.datetime_display.operators = ['>='];
      this.picked_date = new Date(this.query.datetime_display.values[0] * 1000)
        .toISOString().substr(0, 7);
      this.queryTrainings();
    },
    /**
     * Gets the training of the current day by considering all trainings later than today 00:00.
     */
    getDateNow() {
      const dateValue = new Date()
        .setUTCHours(0, 0, 0, 0) / 1000 - 30 * 24 * 60 * 60;
      this.query.datetime_display = {
        values: [Math.round(dateValue)],
        operators: ['>='],
      };
      this.queryTrainings();
    },
    /**
     * Sorts the trainings into different months, e.g.,
     * [
     *  [  # trainings of August
     *    {
     *      datetime_created: "...",
     *      ...
     *      training_id: "...",
     *      weather_daily: "...",
     *      weather_hourly: "..."
     *    },
     *    ...
     *  ],
     *  [  # trainings of September
     *    {
     *      datetime_created: "...",
     *      ...
     *    }
     *  ]
     * ]
     * and checks if weather information is available. If yes, collect three points over the day and
     * display them in the card title.
     * @param {array} trainingArray array of training objects
     */
    sortTrainingData(trainingArray) {
      const trainingArraySorted = [];
      let lastDate = new Date(trainingArray[0].datetime_display);
      let helperArray = [];
      for (let i = 0; i < trainingArray.length; i += 1) {
        const thisDate = new Date(trainingArray[i].datetime_display);
        if (thisDate.getMonth() !== lastDate.getMonth()) {
          trainingArraySorted.push(helperArray);
          helperArray = [];
        }
        if (trainingArray[i].weather_hourly !== null) {
          this.$set(trainingArray[i], 'weather_daily', [
            {
              observation_time: trainingArray[i].weather_hourly[2].observation_time.value,
              weather_code: trainingArray[i].weather_hourly[2].weather_code.value,
              temp: trainingArray[i].weather_hourly[2].temp.value,
            },
            {
              observation_time: trainingArray[i].weather_hourly[5].observation_time.value,
              weather_code: trainingArray[i].weather_hourly[5].weather_code.value,
              temp: trainingArray[i].weather_hourly[5].temp.value,
            },
            {
              observation_time: trainingArray[i].weather_hourly[8].observation_time.value,
              weather_code: trainingArray[i].weather_hourly[8].weather_code.value,
              temp: trainingArray[i].weather_hourly[8].temp.value,
            },
          ]);
        } else {
          this.$set(trainingArray[i], 'weather_daily', []);
        }
        helperArray.push(trainingArray[i]);
        lastDate = thisDate;
      }
      trainingArraySorted.push(helperArray);
      this.training_array_sorted = trainingArraySorted;
    },
    /**
     * Gets the training of the current month by considering all trainings between the 1st of the
     * current month 00:00:00 and the end of the current month 23:59:59
     */
    getDateThisMonth() {
      const year = new Date().getFullYear();
      const monthStart = new Date().getMonth();
      const monthEnd = new Date().getMonth() + 1;
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(23, 59, 59, 59),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      this.query.datetime_display = {
        values: [Math.round(dateStart), Math.round(dateEnd)],
        operators: ['>=', '<='],
      };
      this.queryTrainings();
    },
    /**
     * Gets the training of the previous month by considering all trainings between the 1st of the
     * previous month 00:00:00 and the end of the previous month 23:59:59
     */
    getDateLastMonth() {
      const year = new Date().getFullYear();
      const monthStart = new Date().getMonth() - 1;
      const monthEnd = new Date().getMonth();
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(23, 59, 59, 59),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      this.query.datetime_display = {
        values: [Math.round(dateStart), Math.round(dateEnd)],
        operators: ['>=', '<='],
      };
      this.queryTrainings();
    },
    /**
     * Gets the training of the current year by considering all trainings between the 1st of January
     * 00:00:00 and the end of the current month 23:59:59
     */
    getDateThisYear() {
      const year = new Date().getFullYear();
      const monthStart = 0;
      const monthEnd = new Date().getMonth() + 1;
      const dateStart = new Date(
        new Date().setUTCHours(0, 0, 0, 0),
      ).setUTCFullYear(year, monthStart, 1) / 1000;
      const dateEnd = new Date(
        new Date().setUTCHours(23, 59, 59, 590),
      ).setUTCFullYear(year, monthEnd, 0) / 1000;
      this.query.datetime_display = {
        values: [Math.round(dateStart), Math.round(dateEnd)],
        operators: ['>=', '<='],
      };
      this.queryTrainings();
    },
  },
};
</script>

<style scoped>

</style>
