<template>
  <div>
    <v-card
      class="secondary ml-n6"
      dark
    >
      <v-card-title
        style="height: 100%"
        class="pl-3 py-0 pr-0"
        @click="show_training = !show_training"
      >
        <span
          :style="{ 'font-size': 14 + 'px', 'width': location_width + 'px'}"
        >
          {{ trainingItem.location }}
        </span>
        <TimelineCardTitleWeather
          v-if="trainingItem.weather_daily !== null"
          :weather-daily="trainingItem.weather_daily"
        />
        <span
          style="font-size: 14px; width: 76px"
        >
          {{ trainingItem.datetime_display | formatDate }}
        </span>
        <v-avatar
          class="mr-n2 ml-n3"
          icon
        >
          <v-icon>{{ show_training ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-avatar>
      </v-card-title>
      <v-expand-transition>
        <div v-show="show_training">
          <v-card-text class="white text--primary pa-1">
            <TimelineCardWeather
              v-if="trainingItem.weather_hourly !== null"
              :weather-array="trainingItem.weather_hourly"
            />
          </v-card-text>
          <TimelineCardTable
            :training-item="trainingItem"
          />
          <v-card-actions class="pa-1">
            <v-spacer />
            <v-btn
              fab
              x-small
              color="warning"
              @click="onTrainingEdit()"
            >
              <v-icon>
                mdi-pencil
              </v-icon>
            </v-btn>
            <v-btn
              fab
              x-small
              color="error"
              @click="onTrainingDelete()"
            >
              <v-icon>
                mdi-delete
              </v-icon>
            </v-btn>
          </v-card-actions>
        </div>
      </v-expand-transition>
    </v-card>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'training entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deleteTrainingData()"
    />
  </div>
</template>

<script>
import TimelineCardTable from './TimelineCardTable.vue';
import TimelineCardWeather from './TimelineCardWeather.vue';
import TimelineCardTitleWeather from './TimelineCardTitleWeather.vue';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';
import { apiDeleteTrainingItem } from '../../components/api/TrainingApi';
import { apiDeleteSetupItem } from '../../components/api/SetupApi';

export default {
  name: 'TimelineCard',
  components: {
    TimelineCardTitleWeather,
    ConfirmDeleteDialog,
    TimelineCardWeather,
    TimelineCardTable,
  },
  props: {
    trainingItem: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    show_training: false,
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
    location_width() {
      if (window.innerWidth < 400) {
        return 115;
      }
      return 150;
    },
  },
  methods: {
    /**
     * Emits a message to the parent component that the edit training button was clicked and parses
     * the id of this training.
     */
    onTrainingEdit() {
      this.$store.commit('setTrainingEditId', this.trainingItem.training_id);
    },
    /**
     * Opens the confirm deletion dialog after clicking the delete button of a training.
     */
    onTrainingDelete() {
      this.confirm_delete_dialog = true;
    },
    /**
     * Deletes a training by firstly, deleting all corresponding setups and secondly, deleting the
     * respective training.
     */
    deleteTrainingData() {
      for (let i = 0; i < this.trainingItem.setups.length; i += 1) {
        const setupId = this.trainingItem.setups[i].setup_id;
        if (setupId !== null) {
          apiDeleteSetupItem(setupId);
        }
      }
      const trainingId = this.trainingItem.training_id;
      apiDeleteTrainingItem(trainingId)
        .then(() => {
          this.$emit('removedTraining', trainingId);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: 'Training deleted!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>
