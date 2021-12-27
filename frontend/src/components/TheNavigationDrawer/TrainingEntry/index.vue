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
      @deletionConfirmed="initTrainingForm()"
    />
  </div>
</template>

<script>
import {
  indexOfObjectValueInArray,
  initObject,
} from '../../utils/FromUtils';
import TrainingDialog from './TrainingDialog.vue';
import { apiGetTrainingItem, apiQueryTrainings } from '../../api/TrainingApi';

export default {
  name: 'TheNavigationDrawerTraining',
  components: {
    TrainingDialog,
  },
  data: () => ({
    training_form_object: {
      training_id: null,
      race_track: null,
      weather: null,
      date: null,
      setup_fixed: [
        {
          setup_id: null,
          weather_current: null,
          comment: null,
          time: null,
          operating_hours: null,
          slick_pressure_front: null,
          slick_pressure_rear: null,
          rain_pressure_front: null,
          rain_pressure_rear: null,
        },
      ],
      setup_individual: [],
      sessions: [],
    },
    setup_fixed_template: {
      setup_id: null,
      weather_current: null,
      comment: null,
      time: null,
      operating_hours: null,
      slick_pressure_front: null,
      slick_pressure_rear: null,
      rain_pressure_front: null,
      rain_pressure_rear: null,
    },
    setup_individual_template: [],
  }),
  computed: {
    bike_array: {
      get() {
        return this.$store.getters.getAllBikes;
      },
      set(value) {
        this.$store.commit('setAllBikes', value);
      },
    },
  },
  created() {
    this.$store.subscribe((mutation) => {
      if (mutation.type === 'setTrainingEditId') {
        if (this.$store.getters.getTrainingEditId !== null) {
          this.editTraining();
        }
      }
    });
  },
  methods: {
    /**
     * Checks if a training is active in the vuex store and get the training entry from the
     * database. Otherwise, query the database for a training of the current day
     */
    editTraining() {
      const trainingId = this.$store.getters.getTrainingEditId;
      if (trainingId !== null) {
        apiGetTrainingItem(trainingId)
          .then((res) => {
            this.$store.commit('setTrainingDialogState', true);
            this.compileTrainingData(res.data);
          });
      } else {
        const query = {
          datetime_display: {
            values: [Math.round(new Date().setUTCHours(0, 0, 0, 0) / 1000)],
            operators: ['>='],
          },
        };
        apiQueryTrainings(query)
          .then((res) => {
            if (res.data.length > 0) {
              this.compileTrainingData(res.data[0]);
            } else {
              this.initTrainingForm();
              this.$store.commit('setTrainingDialogSetupTabs', 1);
              this.$store.commit('setTrainingDialogSetupActiveTab', 0);
            }
            this.$store.commit('setTrainingDialogState', true);
          })
          .catch((error) => {
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
          });
      }
    },
    /**
     * Initializes the training dialog form.
     */
    initTrainingForm() {
      initObject(this.training_form_object, null);
      this.training_form_object.date = new Date().toISOString().substr(0, 10);
      this.initTrainingFormSetup();
      this.$store.commit('setTrainingDialogSetupPanel', 0);
      this.$store.commit('setTrainingDialogSetupTabs', 1);
      this.$store.commit('setTrainingDialogSetupActiveTab', 0);
    },
    /**
     * Initializes the setup data of a training.
     */
    initTrainingFormSetup() {
      const bikeIndex = indexOfObjectValueInArray(
        this.bike_array, this.$store.getters.getCurrentBikeId,
      );
      this.training_form_object.setup_fixed = [];
      this.training_form_object.setup_fixed.push(this._.cloneDeep(this.setup_fixed_template));
      this.training_form_object.setup_fixed[0].time = new Date().toTimeString().substr(0, 5);
      this.training_form_object.setup_fixed[0].operating_hours = this
        .$store.getters.getCurrentBikeOperatingHours;
      if (this.bike_array[bikeIndex].setup != null) {
        this.training_form_object.setup_individual = [
          this._.cloneDeep(this.bike_array[bikeIndex].setup),
        ];
        [this.setup_individual_template] = this.training_form_object.setup_individual;
      } else {
        this.training_form_object.setup_individual = [];
      }
      this.training_form_object.sessions = [];
    },
    /**
     * Compile the training data collected from the database to the training dialog form.
     * @param {object} data data of the database
     */
    compileTrainingData(data) {
      this.training_form_object.training_id = data.training_id;
      this.training_form_object.race_track = data.location;
      this.training_form_object.date = this.$options.filters
        .formatDateTime(data.datetime_display).substring(0, 10);
      const numberOfSetups = data.setups.length;
      let numberOfSessions = 0;
      if (numberOfSetups > 0) {
        this.training_form_object.setup_fixed = [];
        this.$store.commit('setTrainingDialogSetupTabs', numberOfSetups);
        this.$store.commit('setTrainingDialogSetupActiveTab', numberOfSetups - 1);
        for (let i = 0; i < numberOfSetups; i += 1) {
          this.training_form_object.setup_fixed.push(this._.cloneDeep(this.setup_fixed_template));
          this.training_form_object.setup_fixed[i].setup_id = data
            .setups[i].setup_id;
          this.training_form_object.setup_fixed[i].comment = data
            .setups[i].comment;
          this.training_form_object.setup_fixed[i].time = this.$options.filters
            .formatDateTime(data.setups[i].datetime_display).substring(11, 16);
          this.training_form_object.setup_fixed[i].operating_hours = data
            .setups[i].operating_hours;
          this.training_form_object.setup_fixed[i].slick_pressure_front = data
            .setups[i].slick_pressure_front;
          this.training_form_object.setup_fixed[i].slick_pressure_rear = data
            .setups[i].slick_pressure_rear;
          this.training_form_object.setup_fixed[i].rain_pressure_front = data
            .setups[i].rain_pressure_front;
          this.training_form_object.setup_fixed[i].rain_pressure_rear = data
            .setups[i].rain_pressure_rear;
          this.training_form_object.setup_fixed[i].rain_pressure_rear = data
            .setups[i].rain_pressure_rear;
          this.$set(this.training_form_object.setup_individual, i, data.setups[i].setup);
          const { sessions } = data.setups[i];
          sessions.map((o) => Object.assign(o, { setup_no: i + 1 }));
          this.training_form_object.sessions.push(...sessions);
          numberOfSessions += data.setups[i].sessions.length;
        }
      } else {
        this.initTrainingFormSetup();
        this.$store.commit('setTrainingDialogSetupTabs', 1);
        this.$store.commit('setTrainingDialogSetupActiveTab', 0);
      }
      this.$store.commit('setTrainingDialogSessionTabs', numberOfSessions);
      this.$store.commit('setTrainingDialogSessionActiveTab', numberOfSessions - 1);
    },
  },
};
</script>
