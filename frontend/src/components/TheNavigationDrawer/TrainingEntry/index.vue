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
import { apiQueryTrainings } from '../../api/TrainingApi';

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
  updated() {
  },
  created() {
  },
  methods: {
    editTraining() {
      const query = {
        datetime_display: {
          value: Math.round(new Date().setUTCHours(0, 0, 0, 0) / 1000),
          operator: '>=',
        },
      };
      apiQueryTrainings(query)
        .then((res) => {
          if (res.data.length > 0) {
            this.training_form_object.training_id = res.data[0].training_id;
            this.training_form_object.race_track = res.data[0].location;
            this.training_form_object.date = this.$options.filters
              .formatDateTime(res.data[0].datetime_display).substring(0, 10);
            this.training_form_object.setup_fixed = [];
            this.$store.commit('setTrainingDialogSetupTabs', res.data[0].setups.length);
            for (let i = 0; i < res.data[0].setups.length; i += 1) {
              this.training_form_object.setup_fixed
                .push(this._.cloneDeep(this.setup_fixed_template));
              this.training_form_object.setup_fixed[i].setup_id = res.data[0]
                .setups[i].setup_id;
              this.training_form_object.setup_fixed[i].comment = res.data[0]
                .setups[i].comment;
              this.training_form_object.setup_fixed[i].time = this.$options.filters
                .formatDateTime(res.data[0].setups[i].datetime_display).substring(11, 16);
              this.training_form_object.setup_fixed[i].operating_hours = res.data[0]
                .setups[i].operating_hours;
              this.training_form_object.setup_fixed[i].slick_pressure_front = res.data[0]
                .setups[i].slick_pressure_front;
              this.training_form_object.setup_fixed[i].slick_pressure_rear = res.data[0]
                .setups[i].slick_pressure_rear;
              this.training_form_object.setup_fixed[i].rain_pressure_front = res.data[0]
                .setups[i].rain_pressure_front;
              this.training_form_object.setup_fixed[i].rain_pressure_rear = res.data[0]
                .setups[i].rain_pressure_rear;
              this.training_form_object.setup_fixed[i].rain_pressure_rear = res.data[0]
                .setups[i].rain_pressure_rear;
              this.training_form_object.setup_individual[i] = res.data[0]
                .setups[i].setup;
            }
          } else {
            this.initTrainingForm();
          }
          this.$store.commit('setTrainingDialogState', true);
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error} - Database connection failed!`,
          });
        });
    },
    initTrainingForm() {
      const bikeIndex = indexOfObjectValueInArray(
        this.bike_array, this.$store.getters.getCurrentBikeId,
      );
      initObject(this.training_form_object, null);
      this.training_form_object.date = new Date().toISOString().substr(0, 10);
      this.training_form_object.setup_fixed = [this._.cloneDeep(this.setup_fixed_template)];
      this.training_form_object.setup_fixed[0].time = new Date().toTimeString().substr(0, 5);
      this.training_form_object.setup_fixed[0].operating_hours = this
        .$store.getters.getCurrentBikeOperatingHours;
      if (this.bike_array[bikeIndex].setup != null) {
        this.training_form_object.setup_individual = [
          this._.cloneDeep(this.bike_array[bikeIndex].setup),
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
