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
        <v-list-item
          v-for="(bike, index) in bike_array"
          :key="bike.bike_id + '_list'"
          v-touch="{ right: () => editBike(bike.bike_id) }"
          @click="selectBike(index)"
        >
          <v-list-item-action>
            <v-radio
              :key="bike.bike_id + '_radio'"
              :value="bike.bike_id"
            />
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
      :bike-form-object="bike_form_object"
      :setup-individual-template="setup_individual_template"
      :operating-hours-initial="operating_hours_initial"
      @clearBikeDialog="initBikeForm"
    />
  </div>
</template>

<script>
import {
  indexOfObjectValueInArray,
  initObject,
} from '../../utils/FromUtils';
import TheNavigationDrawerBikeDialog from './BikeDialog.vue';

export default {
  name: 'TheNavigationDrawerBike',
  components: {
    TheNavigationDrawerBikeDialog,
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
      slick_front_name: null,
      slick_front_notes: null,
      slick_front_pressure: [],
      slick_rear_name: null,
      slick_rear_notes: null,
      slick_rear_pressure: [],
      rain_front_name: null,
      rain_front_notes: null,
      rain_front_pressure: [],
      rain_rear_name: null,
      rain_rear_notes: null,
      rain_rear_pressure: [],
      setup_individual: [
        {
          category: null,
          group: null,
          name: null,
          ticks_current: null,
          ticks_standard: null,
          ticks_available: null,
        },
      ],
    },
    setup_individual_template: {
      category: null,
      group: null,
      name: null,
      ticks_current: null,
      ticks_standard: null,
      ticks_available: null,
    },
    operating_hours_initial: 0,
  }),
  computed: {
    selected_bike: {
      get() {
        return this.$store.getters.getCurrentBikeId;
      },
      set(value) {
        this.selectBike(value);
      },
    },
    bike_array: {
      get() {
        return this.$store.getters.getAllBikes;
      },
      set(value) {
        this.$store.commit('setAllBikes', value);
      },
    },
    current_bike_id: {
      get() {
        return this.$store.getters.getCurrentBikeId;
      },
      set(value) {
        this.$store.commit('setCurrentBikeId', value);
      },
    },
    bike_edit_flag: {
      get() {
        return this.$store.getters.getBikeEditFlag;
      },
      set(value) {
        this.$store.commit('setBikeEditFlag', value);
      },
    },
    bike_dialog: {
      get() {
        return this.$store.getters.getBikeDialogState;
      },
      set(value) {
        this.$store.commit('setBikeDialogState', value);
      },
    },
    navigation_drawer: {
      get() {
        return this.$store.getters.getNavigationDrawerState;
      },
      set(value) {
        this.$store.commit('setNavigationDrawerState', value);
      },
    },
  },
  methods: {
    selectBike(index) {
      const selectedBike = this.bike_array[index];
      if (typeof index === 'number') {
        this.$nextTick(() => {
          if (this.current_bike_id !== selectedBike.bike_id && this.bike_dialog === false) {
            this.$store.commit('selectBike', selectedBike);
            this.navigation_drawer = false;
            this.$forceUpdate();
          }
        });
      }
    },
    editBike(BikeId) {
      this.bike_edit_flag = true;
      this.bike_dialog = true;
      const bikeIndex = indexOfObjectValueInArray(this.bike_array, BikeId);
      this.operating_hours_initial = this.bike_array[bikeIndex].operating_hours;
      this.bike_form_object.bike_id = this.bike_array[bikeIndex].bike_id;
      this.bike_form_object.manufacturer = this.bike_array[bikeIndex].manufacturer;
      this.bike_form_object.model = this.bike_array[bikeIndex].model;
      this.bike_form_object.year = this.bike_array[bikeIndex].year;
      this.bike_form_object.operating_hours = this.bike_array[bikeIndex].operating_hours;
      this.bike_form_object.ccm = this.bike_array[bikeIndex].ccm;
      this.bike_form_object.stroke = this.bike_array[bikeIndex].stroke;
      this.bike_form_object.piston = this.bike_array[bikeIndex].piston;
      this.bike_form_object.slick_front_name = this.bike_array[bikeIndex].slick_front_name;
      this.bike_form_object.slick_front_notes = this.bike_array[bikeIndex].slick_front_notes;
      this.bike_form_object.slick_front_pressure = this.bike_array[bikeIndex].slick_front_pressure;
      this.bike_form_object.slick_rear_name = this.bike_array[bikeIndex].slick_rear_name;
      this.bike_form_object.slick_rear_notes = this.bike_array[bikeIndex].slick_rear_notes;
      this.bike_form_object.slick_rear_pressure = this.bike_array[bikeIndex].slick_rear_pressure;
      this.bike_form_object.rain_front_name = this.bike_array[bikeIndex].rain_front_name;
      this.bike_form_object.rain_front_notes = this.bike_array[bikeIndex].rain_front_notes;
      this.bike_form_object.rain_front_pressure = this.bike_array[bikeIndex].rain_front_pressure;
      this.bike_form_object.rain_rear_name = this.bike_array[bikeIndex].rain_rear_name;
      this.bike_form_object.rain_rear_notes = this.bike_array[bikeIndex].rain_rear_notes;
      this.bike_form_object.rain_rear_pressure = this.bike_array[bikeIndex].rain_rear_pressure;
      if (this.bike_array[bikeIndex].setup === null) {
        this.bike_form_object.setup_individual = [this._.cloneDeep(this.setup_individual_template)];
      } else {
        this.bike_form_object.setup_individual = this.bike_array[bikeIndex].setup;
      }
    },
    createBike() {
      this.bike_dialog = true;
      this.navigation_drawer = false;
    },
    initBikeForm() {
      initObject(this.bike_form_object, null);
      this.bike_form_object.slick_front_pressure = [];
      this.bike_form_object.slick_rear_pressure = [];
      this.bike_form_object.rain_front_pressure = [];
      this.bike_form_object.rain_rear_pressure = [];
      this.bike_form_object.setup_individual = [this._.cloneDeep(this.setup_individual_template)];
      this.bike_edit_flag = false;
    },
  },
};
</script>
