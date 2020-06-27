<template>
  <div>
    <v-dialog v-model="bike_dialog" fullscreen hide-overlay
              transition="dialog-bottom-transition">
      <v-form
        v-model="valid_bike_dialog"
        ref="validation_bike_form"
      >
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click.prevent="onBikeCancel">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Motorbike settings</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn
                text
                @click.prevent="confirm_delete_dialog = true"
              >Delete</v-btn>
            </v-toolbar-items>
            <v-toolbar-items>
              <v-btn
                text
                @click.prevent="onBikeSubmit"
                :disabled="!valid_bike_dialog"
              >Save</v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <BikeDialogRequired
            :bike_form_object="bike_form_object"
          />
          <v-divider></v-divider>
          <BikeDialogOptional
            :bike_form_object="bike_form_object"
          />
          <v-divider></v-divider>
          <BikeDialogSetup
            :bike_form_object="bike_form_object"
            :setup_individual="bike_form_object.setup_individual"
            :setup_individual_template="setup_individual_template"
          />
        </v-card>
      </v-form>
    </v-dialog>
    <ConfirmDeleteDialog
      :flagged_for_deletion="'bike entry'"
      :confirm_delete_dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deleteBikeData"
    />
  </div>
</template>

<script>
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog';
import {BikeApi} from '../../api/BikeApi';
import BikeDialogSetup from './BikeDialogSetup';
import BikeDialogOptional from './BikeDialogOptional';
import BikeDialogRequired from './BikeDialogRequired';

export default {
  name: 'TheNavigationDrawerBikeDialog',
  props: {
    bike_array: {
      type: Array,
      required: true,
    },
    bike_form_object: {
      type: Object,
      required: true,
    },
    setup_individual_template: {
      type: Object,
      required: true,
    }
  },
  components: {
    BikeDialogRequired,
    BikeDialogOptional,
    BikeDialogSetup,
    ConfirmDeleteDialog,
  },
  data: () => ({
    valid_bike_dialog: true,
    confirm_delete_dialog: false,
    setup_entries: 1,
  }),
  computed: {
    bike_dialog: {
      get() {
        return this.$store.getters.getBikeDialogState
      },
      set(value) {
        this.$store.commit('setBikeDialogState', value)
      },
    },
  },
  methods: {
    updatedBike() {
      this.$emit('updatedBike');
    },
    postBikeData(payload) {
      BikeApi.postBike(BikeId, payload).then(() => this.updatedBike());
    },
    async putBikeData(BikeId, payload) {
      BikeApi.putBike(BikeId, payload).then(() => this.updatedBike());
    },
    deleteBikeData() {
      BikeApi.deleteBike(this.bike_form_object.bike_id).then(() => this.updatedBike());
      this.$emit('clearBikeDialog');
      this.$store.commit('setBikeDialogState', false);
    },
    async onBikeSubmit() {
      const BikeId = this.bike_form_object.bike_id;
      const payload = {
        operating_hours: this.bike_form_object.operating_hours,
        manufacturer: this.bike_form_object.manufacturer,
        model: this.bike_form_object.model,
        year: this.bike_form_object.year,
        ccm: this.bike_form_object.ccm,
        stroke: this.bike_form_object.stroke,
        piston: this.bike_form_object.piston,
        slick_front: this.bike_form_object.slick_front,
        slick_rear: this.bike_form_object.slick_rear,
        rain_front: this.bike_form_object.rain_front,
        rain_rear: this.bike_form_object.rain_rear,
        setup: this.bike_form_object.setup_individual,
      };
      if (this.$store.getters.getBikeEditFlag === false) {
        await this.postBikeData(payload);
      } else {
        await this.putBikeData(BikeId, payload);
        if (this.$store.getters.getCurrentBikeId === BikeId) {
          payload.bike_id = BikeId;
          this.$store.commit('selectBike', payload);
          this.$forceUpdate();
        }
      }
      this.$store.commit('setBikeDialogState', false);
    },
    onBikeCancel() {
      if (typeof this.$refs.validation_bike_form !== 'undefined') {
        this.$refs.validation_bike_form.resetValidation();
      }
      this.$store.commit('setBikeDialogState', false);
      this.$emit('clearBikeDialog');
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
