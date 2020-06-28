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
    <TheNavigationDrawerTrainingDialog
      :setup_fixed_template="setup_fixed_template"
      :setup_individual_template="setup_individual_template"
      :training_form_object="training_form_object"
    />
  </div>
</template>

<script>
import TheNavigationDrawerTrainingDialog from './TrainingDialog';
import {FormUtils} from '../../utils/FromUtils';
import _ from 'lodash';

export default {
  name: 'TheNavigationDrawerTraining',
  props: {
    bike_array: {
      type: Array,
      required: true,
    },
  },
  components: {
    TheNavigationDrawerTrainingDialog,
  },
  data: () => ({
    training_form_object: {
      race_track: null,
      date: null,
      setup_fixed: [
        {
          operating_hours: null,
          slick_pressure_front: null,
          slick_pressure_rear: null,
          rain_pressure_front: null,
          rain_pressure_rear: null,
        },
      ],
      setup_individual: null,
    },
    setup_fixed_template: {
      operating_hours: null,
      slick_pressure_front: null,
      slick_pressure_rear: null,
      rain_pressure_front: null,
      rain_pressure_rear: null,
    },
    setup_individual_template: [],
  }),
  methods: {
    editTraining() {
      this.$store.commit('setTrainingDialogState', true);
      this.initTrainingForm();
    },
    initTrainingForm() {
      const bike_index = FormUtils.indexOfObjectValueInArray(
        this.bike_array,this.$store.getters.getCurrentBikeId)
      FormUtils.initObject(this.training_form_object, null);
      this.training_form_object.setup_fixed = [_.cloneDeep(this.setup_fixed_template)];
      if (this.bike_array[bike_index].setup != null) {
        this.training_form_object.setup_individual = [_.cloneDeep(this.bike_array[bike_index].setup)];
      }
      for (let i = 0;
           i < Object.values(this.training_form_object.setup_individual)[0].length;
           i += 1) {
        this.training_form_object.setup_individual[0][i] = Object.assign(
          this.training_form_object.setup_individual[0][i],
          {'ticks_current': _.cloneDeep(
            this.training_form_object.setup_individual[0][i].ticks_standard)
          },
        )
      }
      this.setup_individual_template = this.training_form_object.setup_individual[0];
      this.$store.commit('setTrainingDialogSetupPanel', 0)
      this.$store.commit('setTrainingDialogSetupTabs', 1)
      this.$store.commit('setTrainingDialogSetupActiveTab', 0)
    },
  },
  updated() {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
