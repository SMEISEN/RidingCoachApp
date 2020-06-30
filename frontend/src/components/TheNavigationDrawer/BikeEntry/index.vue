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
          v-for="(bike, index) in bikeArray"
          :key="index"
          v-touch="{ right: () => editBike(bike.bike_id) }"
          @click="selectBike(index)"
        >
          <v-list-item-action>
            <v-radio
              :key="bike.bike_id"
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
      :bike-array="bikeArray"
      @clearBikeDialog="initBikeForm"
      @updatedBike="updatedBike()"
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
  props: {
    bikeArray: {
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
          group: null,
          name: null,
          ticks_available: null,
          ticks_standard: null,
          ticks_current: null,
        },
      ],
    },
    setup_individual_template: {
      category: null,
      group: null,
      name: null,
      ticks_available: null,
      ticks_standard: null,
    },
  }),
  computed: {
    selected_bike: {
      get() {
        return this.$store.getters.getCurrentBikeId;
      },
      set(value) {
        this.$store.commit('selectBike', value);
      },
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    updatedBike() {
      this.$emit('updated');
    },
    selectBike(index) {
      const selectedBike = this.bikeArray[index];
      this.selected_bike = selectedBike.bike_id;
      this.$store.commit('selectBike', selectedBike);
      this.$forceUpdate();
    },
    editBike(BikeId) {
      const bikeIndex = indexOfObjectValueInArray(this.bikeArray, BikeId);
      this.bike_form_object.bike_id = this.bikeArray[bikeIndex].bike_id;
      this.bike_form_object.manufacturer = this.bikeArray[bikeIndex].manufacturer;
      this.bike_form_object.model = this.bikeArray[bikeIndex].model;
      this.bike_form_object.year = this.bikeArray[bikeIndex].year;
      this.bike_form_object.operating_hours = this.bikeArray[bikeIndex].operating_hours;
      this.bike_form_object.ccm = this.bikeArray[bikeIndex].ccm;
      this.bike_form_object.stroke = this.bikeArray[bikeIndex].stroke;
      this.bike_form_object.piston = this.bikeArray[bikeIndex].piston;
      this.bike_form_object.slick_front = this.bikeArray[bikeIndex].slick_front;
      this.bike_form_object.slick_rear = this.bikeArray[bikeIndex].slick_rear;
      this.bike_form_object.rain_front = this.bikeArray[bikeIndex].rain_front;
      this.bike_form_object.rain_rear = this.bikeArray[bikeIndex].rain_rear;
      if (this.bikeArray[bikeIndex].setup === null) {
        this.bike_form_object.setup_individual = [this._.cloneDeep(this.setup_individual_template)];
      } else {
        this.bike_form_object.setup_individual = this.bikeArray[bikeIndex].setup;
      }
      this.$store.commit('setBikeEditFlag', true);
      this.$store.commit('setBikeDialogState', true);
      this.$store.commit('setNavigationDrawerState', false);
    },
    createBike() {
      this.$store.commit('setBikeDialogState', true);
      this.$store.commit('setNavigationDrawerState', false);
    },
    initBikeForm() {
      initObject(this.bike_form_object, null);
      this.bike_form_object.setup_individual = [this._.cloneDeep(this.setup_individual_template)];
      this.$store.commit('setBikeEditFlag', false);
    },
  },
};
</script>

<style scoped>

</style>
