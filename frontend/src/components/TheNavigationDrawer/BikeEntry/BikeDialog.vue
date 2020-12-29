<template>
  <div>
    <v-dialog
      v-model="bike_dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-form
        v-if="bike_dialog"
        ref="validation_bike_form"
        v-model="valid_bike_dialog"
      >
        <v-card :min-height="window_height">
          <v-toolbar
            dark
            color="primary"
          >
            <v-btn
              icon
              @click.prevent="onBikeCancel()"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Motorbike settings</v-toolbar-title>
            <v-spacer />
            <v-toolbar-items>
              <v-btn
                text
                @click.prevent="confirm_delete_dialog = true"
              >
                Delete
              </v-btn>
            </v-toolbar-items>
            <v-toolbar-items>
              <v-btn
                text
                :disabled="!valid_bike_dialog"
                @click.prevent="onBikeSubmit()"
              >
                Save
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <BikeDialogRequired
            :bike-form-object="bikeFormObject"
          />
          <v-divider />
          <BikeDialogOptional
            :bike-form-object="bikeFormObject"
          />
          <v-divider />
          <BikeDialogSetup
            :bike-form-object="bikeFormObject"
            :setup-individual="bikeFormObject.setup_individual"
            :setup-individual-template="setupIndividualTemplate"
          />
        </v-card>
      </v-form>
    </v-dialog>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'bike entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deleteBikeData()"
    />
  </div>
</template>

<script>
import {
  apiPostBike,
  apiPutBike,
  apiDeleteBike,
} from '../../api/BikeApi';
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';
import BikeDialogSetup from './BikeDialogSetup.vue';
import BikeDialogOptional from './BikeDialogOptional.vue';
import BikeDialogRequired from './BikeDialogRequired.vue';
import {
  indexOfObjectValueInArray,
} from '../../utils/FromUtils';

export default {
  name: 'TheNavigationDrawerBikeDialog',
  components: {
    BikeDialogRequired,
    BikeDialogOptional,
    BikeDialogSetup,
    ConfirmDeleteDialog,
  },
  props: {
    bikeFormObject: {
      type: Object,
      required: true,
    },
    setupIndividualTemplate: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    valid_bike_dialog: true,
    confirm_delete_dialog: false,
    setup_entries: 1,
    window_height: 0,
  }),
  computed: {
    bike_dialog: {
      get() {
        return this.$store.getters.getBikeDialogState;
      },
      set(value) {
        this.$store.commit('setBikeDialogState', value);
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
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
  },
  methods: {
    postBike(payload) {
      apiPostBike(payload)
        .then((res) => {
          const newBike = payload;
          newBike.bike_id = res.data;
          this.$store.commit('selectBike', newBike);
          this.$forceUpdate();
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Bike created!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}`,
          });
        });
    },
    putBike(BikeId, payload) {
      apiPutBike(BikeId, payload)
        .then(() => {
          const bikeIndex = indexOfObjectValueInArray(this.bike_array, BikeId);
          this.bike_array[bikeIndex] = payload;
          this.$store.commit('selectBike', payload);
          this.$forceUpdate();
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Bike edited!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}`,
          });
        });
    },
    deleteBikeData() {
      const bikeId = this.bikeFormObject.bike_id;
      apiDeleteBike(bikeId)
        .then(() => {
          this.bike_array = this.bike_array.filter((x) => x.bike_id !== bikeId);
          this.$store.commit('selectBike', this.bike_array[0]);
          this.$forceUpdate();
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: 'Bike deleted!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}`,
          });
        });
      this.$emit('clearBikeDialog');
      this.$store.commit('setBikeDialogState', false);
      this.$store.commit('setNavigationDrawerState', false);
    },
    onBikeSubmit() {
      const BikeId = this.bikeFormObject.bike_id;
      const payload = {
        operating_hours: this.bikeFormObject.operating_hours,
        manufacturer: this.bikeFormObject.manufacturer,
        model: this.bikeFormObject.model,
        year: this.bikeFormObject.year,
        ccm: this.bikeFormObject.ccm,
        stroke: this.bikeFormObject.stroke,
        piston: this.bikeFormObject.piston,
        slick_front_name: this.bikeFormObject.slick_front_name,
        slick_front_notes: this.bikeFormObject.slick_front_notes,
        slick_front_pressure: this.bikeFormObject.slick_front_pressure,
        slick_rear_name: this.bikeFormObject.slick_rear_name,
        slick_rear_notes: this.bikeFormObject.slick_rear_notes,
        slick_rear_pressure: this.bikeFormObject.slick_rear_pressure,
        rain_front_name: this.bikeFormObject.rain_front_name,
        rain_front_notes: this.bikeFormObject.rain_front_notes,
        rain_front_pressure: this.bikeFormObject.rain_front_pressure,
        rain_rear_name: this.bikeFormObject.rain_rear_name,
        rain_rear_notes: this.bikeFormObject.rain_rear_notes,
        rain_rear_pressure: this.bikeFormObject.rain_rear_pressure,
        setup: this.bikeFormObject.setup_individual,
      };
      if (this.$store.getters.getBikeEditFlag === false) {
        this.postBike(payload);
      } else {
        payload.bike_id = BikeId;
        this.putBike(BikeId, payload);
      }
      this.$store.commit('setBikeEditFlag', false);
      this.$store.commit('setBikeDialogState', false);
      this.$store.commit('setNavigationDrawerState', false);
    },
    onBikeCancel() {
      if (typeof this.$refs.validation_bike_form !== 'undefined') {
        this.$refs.validation_bike_form.resetValidation();
      }
      this.$store.commit('setBikeDialogState', false);
      this.$emit('clearBikeDialog');
    },
  },
};
</script>

<style scoped>

</style>
