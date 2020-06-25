<template>
  <div>
    <v-list-group
      prepend-icon="mdi-motorbike"
      nav
      dense
      active-class="primary--text text--accent"
    >
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>Bike</v-list-item-title>
        </v-list-item-content>
      </template>
      <v-radio-group v-model="selected_bike">
        <v-list-item v-for="(bike, index) in bike_array" :key="index"
                     @click="selectBike(index)"
                     v-touch="{ right: () => editBike(bike.bike_id) }"
        >
          <v-list-item-action>
            <v-radio :value="bike.bike_id" :key="bike.bike_id"></v-radio>
          </v-list-item-action>
          <v-list-item-title>
            {{ bike.manufacturer }} {{ bike.model }} {{ bike.year }}
          </v-list-item-title>
          <v-list-item-icon @click="editBike(bike.bike_id)">
            <v-icon>mdi-settings</v-icon>
          </v-list-item-icon>
        </v-list-item>
        <v-list-item @click="createBike()">
          <v-list-item-action>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-action>
          <v-list-item-action-text>
            Add new bike
          </v-list-item-action-text>
        </v-list-item>
      </v-radio-group>
    </v-list-group>
    <TheNavigationDrawerBikeDialog
      :bike_form_object.sync="bike_form_object"
      :setup_individual_object="setup_individual_object"
      :bike_array="bike_array"
      @clearBikeDialog="initBikeForm"
      @updatedBike="updatedBike()"
    />
  </div>
</template>

<script>
import {FormUtils} from '../../utils/FromUtils';
import TheNavigationDrawerBikeDialog from './BikeDialog';

export default {
  name: 'TheNavigationDrawerBike',
  components: {
    TheNavigationDrawerBikeDialog,
  },
  props: {
    bike_array: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    bike_form_object: {
      bike_id: null,
      manufacturer: null,
      model: null,
      year: null,
      operating_hours: null,
      ccm: null,
      stroke: null,
      piston: null,
      slick_front: null,
      slick_rear: null,
      rain_front: null,
      rain_rear: null,
      setup_individual: [
        {
          category: null,
          name: null,
          ticks_available: null,
          ticks_standard: null,
          ticks_current: null,
        },
      ],
    },
    setup_individual_object: {
      category: null,
      name: null,
      ticks_available: null,
      ticks_standard: null,
    },
    setup_fixed_dict: {
      operating_hours: null,
      slick_pressure_front: null,
      slick_pressure_rear: null,
      rain_pressure_front: null,
      rain_pressure_rear: null,
    },
  }),
  computed: {
    selected_bike: {
      get() {
        return this.$store.getters.getCurrentBikeId
      },
      set(value) {
        this.$store.commit('selectBike', value)
      },
    },
  },
  methods: {
    updatedBike() {
      this.$emit('updated');
    },
    selectBike(index) {
      const selectedBike = this.bike_array[index];
      this.selected_bike = selectedBike.bike_id;
      this.$store.commit('selectBike', selectedBike);
      this.$forceUpdate();
    },
    editBike(BikeId) {
      const bike_index = FormUtils.indexOfObjectValueInArray(this.bike_array, BikeId)
      this.bike_form_object.bike_id = this.bike_array[bike_index].bike_id;
      this.bike_form_object.manufacturer = this.bike_array[bike_index].manufacturer;
      this.bike_form_object.model = this.bike_array[bike_index].model;
      this.bike_form_object.year = this.bike_array[bike_index].year;
      this.bike_form_object.operating_hours = this.bike_array[bike_index].operating_hours;
      this.bike_form_object.ccm = this.bike_array[bike_index].ccm;
      this.bike_form_object.stroke = this.bike_array[bike_index].stroke;
      this.bike_form_object.piston = this.bike_array[bike_index].piston;
      this.bike_form_object.slick_front = this.bike_array[bike_index].slick_front;
      this.bike_form_object.slick_rear = this.bike_array[bike_index].slick_rear;
      this.bike_form_object.rain_front = this.bike_array[bike_index].rain_front;
      this.bike_form_object.rain_rear = this.bike_array[bike_index].rain_rear;
      this.bike_form_object.setup_individual = this.bike_array[bike_index].setup;
      this.$store.commit('setBikeEditFlag', true);
      this.$store.commit('setBikeDialogState', true);
      this.$store.commit('setNavigationDrawerState', false);
    },
    createBike() {
      this.$store.commit('setBikeDialogState', true);
      this.$store.commit('setNavigationDrawerState', false);
    },
    initBikeForm() {
      FormUtils.initObject(this.bike_form_object, null);
      this.bike_form_object.setup_individual = [_.clone(this.setup_individual_object)];
      this.$store.commit('setBikeEditFlag', false);
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
