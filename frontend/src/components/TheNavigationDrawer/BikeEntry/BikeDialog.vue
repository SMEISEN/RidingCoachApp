<template>
  <div>
    <v-dialog
      v-model="bike_dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-form
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

export default {
  name: 'TheNavigationDrawerBikeDialog',
  components: {
    BikeDialogRequired,
    BikeDialogOptional,
    BikeDialogSetup,
    ConfirmDeleteDialog,
  },
  props: {
    bikeArray: {
      type: Array,
      required: true,
    },
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
  },
  updated() {
    this.window_height = window.innerHeight;
  },
  created() {
  },
  methods: {
    postBike(payload) {
      apiPostBike(payload)
        .then(() => {
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
            message: `${error} - Database connection failed!`,
          });
        });
    },
    putBike(BikeId, payload) {
      apiPutBike(BikeId, payload)
        .then(() => {
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
            message: `${error} - Database connection failed!`,
          });
        });
    },
    deleteBikeData() {
      const bikeId = this.bikeFormObject.bike_id;
      apiDeleteBike(bikeId)
        .then(() => {
          const newBikeArray = this.bikeArray.filter((x) => x.bike_id !== bikeId);
          this.$emit('update:bikeArray', newBikeArray);
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
            message: `${error} - Database connection failed!`,
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
        slick_front: this.bikeFormObject.slick_front,
        slick_rear: this.bikeFormObject.slick_rear,
        rain_front: this.bikeFormObject.rain_front,
        rain_rear: this.bikeFormObject.rain_rear,
        setup: this.bikeFormObject.setup_individual,
      };
      if (this.$store.getters.getBikeEditFlag === false) {
        this.postBike(payload);
      } else {
        this.putBike(BikeId, payload);
        if (this.$store.getters.getCurrentBikeId === BikeId) {
          payload.bike_id = BikeId;
          this.$store.commit('selectBike', payload);
          this.$forceUpdate();
        }
      }
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
