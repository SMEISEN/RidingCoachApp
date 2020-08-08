<template>
  <v-card-text>
    <v-timeline
      dense
      clipped
      class="ml-n9"
    >
      <v-timeline-item
        v-for="(activity_item, activity_index) in latest_activity"
        :key="'activity/' + activity_index"
        color="primary"
        small
        fill-dot
      >
        <template v-slot:icon>
          <v-icon
            color="white"
            small
            @click="routeToPage(activity_item)"
          >
            {{ Object.keys(activity_item)
              .includes('location') ? 'mdi-racing-helmet' : 'mdi-calendar-edit' }}
          </v-icon>
        </template>
        <v-row
          no-gutters
          class="ml-n3"
        >
          <v-col
            v-if="Object.keys(activity_item).includes('location')"
            cols="7"
          >
            Training in {{ activity_item.location }}.
          </v-col>
          <v-col
            v-else
            cols="7"
          >
            Maintenance work on
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span
                  v-bind="attrs"
                  v-on="on"
                >
                  {{ activity_item.categories }}.
                </span>
              </template>
              <span class="pre-formatted">
                {{ activity_item.names }}
              </span>
            </v-tooltip>
          </v-col>
          <v-col
            class="text-right"
            cols="5"
          >
            {{ activity_item.datetime_display | formatDate }}
          </v-col>
        </v-row>
      </v-timeline-item>
    </v-timeline>
  </v-card-text>
</template>

<script>
import { apiGetTrainings } from '../../components/api/TrainingApi';
import { apiGetHistory } from '../../components/api/HistoryApi';

export default {
  name: 'DashboardTimeline',
  data: () => ({
    training_array: [],
    history_array: [],
    latest_activity: [],
  }),
  updated() {
  },
  created() {
    this.getTrainingsAndHistory();
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setTrainingDialogState'
        && this.$store.getters.getTrainingDialogState === false) {
        this.getTrainingsAndHistory();
      }
    });
  },
  methods: {
    routeToPage(object) {
      if (Object.keys(object).includes('location')) {
        this.$router.push('/training');
      } else {
        this.$router.push('/history');
      }
    },
    getTrainingsAndHistory() {
      apiGetHistory().then((resHistory) => {
        let lastDay = resHistory.data[0].datetime_display;
        let historyData = {
          categories: [],
          names: [],
          datetime_display: null,
        };
        for (let i = 0; i < resHistory.data.length; i += 1) {
          const currentDay = resHistory.data[i].datetime_display;
          const { category } = resHistory.data[i];
          const { name } = resHistory.data[i];
          historyData.categories.push(category);
          historyData.names.push(name);
          if (lastDay.substr(0, 10) !== currentDay.substr(0, 10)) {
            historyData.categories = this._.uniq(historyData.categories).sort().join(', ');
            historyData.names = this._.uniq(historyData.names).sort().join('\n');
            historyData.datetime_display = lastDay;
            this.history_array.push(historyData);
            historyData = {
              categories: [],
              names: [],
              datetime_display: null,
            };
            lastDay = currentDay;
          }
        }
        apiGetTrainings().then((resTraining) => {
          this.training_array = resTraining.data;
          this.latest_activity = this._.orderBy(
            this.training_array.concat(this.history_array),
            ['datetime_display'],
            ['desc'],
          ).slice(0, 6);
        });
      });
    },
  },
};
</script>

<style scoped>
.pre-formatted {
  white-space: pre-line;
}
</style>
