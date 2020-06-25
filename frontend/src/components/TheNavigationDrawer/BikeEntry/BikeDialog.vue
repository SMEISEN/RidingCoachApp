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
          <v-subheader>Required fields</v-subheader>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" xs="12" sm="4" md="4">
                <v-text-field
                  label="Manufacturer*"
                  :rules="[v => !!v]"
                  required
                  v-model="bike_form_object.manufacturer"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="5" md="6">
                <v-text-field
                  label="Model*"
                  :rules="[v => !!v]"
                  required
                  v-model="bike_form_object.model"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="3" md="2">
                <v-text-field
                  append-outer-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  @click:append-outer="incrementYear"
                  @click:prepend="decrementYear"
                  :rules="[v => !!v]"
                  required
                  label="Year*"
                  v-model="bike_form_object.year"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="9" md="10"></v-col>
              <v-col cols="12" xs="12" sm="3" md="2">
                <v-text-field
                  append-outer-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  @click:append-outer="incrementHour"
                  @click:prepend="decrementHour"
                  :rules="[v => !!v]"
                  required
                  label="Operating hours*"
                  hint="of engine"
                  suffix="h"
                  v-model="bike_form_object.operating_hours">
                </v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
          <v-subheader>Optional fields</v-subheader>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" xs="4" sm="4" md="4">
                <v-text-field
                  label="Engine ccm"
                  v-model="bike_form_object.ccm"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="4" sm="4" md="4">
                <v-text-field
                  label="Engine stroke"
                  v-model="bike_form_object.stroke"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="4" sm="4" md="4">
                <v-text-field
                  label="Engine piston"
                  v-model="bike_form_object.piston"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="6" md="6">
                <v-text-field
                  label="Slick front"
                  v-model="bike_form_object.slick_front"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="6" md="6">
                <v-text-field
                  label="Slick rear"
                  v-model="bike_form_object.slick_rear"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="6" md="6">
                <v-text-field
                  label="Rain front"
                  v-model="bike_form_object.rain_front"
                ></v-text-field>
              </v-col>
              <v-col cols="12" xs="12" sm="6" md="6">
                <v-text-field
                  label="Rain rear"
                  v-model="bike_form_object.rain_rear"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
          <v-subheader>Available setup</v-subheader>
          <v-card-text>
            <v-simple-table dense light>
              <thead>
              <tr>
                <th class="text-left">Category</th>
                <th class="text-left">Name</th>
                <th class="text-left">Available ticks</th>
                <th class="text-left">Standard tick</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(entry, index) in bike_form_object.setup_individual"
                  v-bind:key="index">
                <td style="border-bottom: none"><v-text-field
                  style="font-size: 12px"
                  dense
                  height="20px"
                  v-model="entry.category"
                  single-line />
                </td>
                <td style="border-bottom: none"><v-text-field
                  style="font-size: 12px"
                  dense
                  height="20px"
                  v-model="entry.name"
                  single-line />
                </td>
                <td style="border-bottom: none"><v-text-field
                  style="font-size: 12px"
                  dense
                  height="20px"
                  v-model="entry.ticks_available"
                  single-line />
                </td>
                <td style="border-bottom: none"><v-text-field
                  style="font-size: 12px"
                  dense
                  height="20px"
                  v-model="entry.ticks_standard"
                  single-line />
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </v-card-text>
          <v-card-text style="height: 50px; position: relative">
            <v-btn
              absolute
              small
              fab
              top
              right
              color="primary"
              @click.prevent="addSetupRow"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-text>
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
import {FormUtils} from '../../utils/FromUtils';
import {BikeApi} from '../../api/BikeApi';

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
    setup_individual_object: {
      type: Object,
      required: true,
    }
  },
  components: {
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
    incrementHour() {
      this.bike_form_object.operating_hours = FormUtils
        .incrementNumber(this.bike_form_object.operating_hours, 0.1, 1)
    },
    decrementHour() {
      this.bike_form_object.operating_hours = FormUtils
        .decrementNumber(this.bike_form_object.operating_hours, 0.1, 1)
    },
    incrementYear() {
      this.bike_form_object.year = FormUtils
        .incrementNumber(this.bike_form_object.year, 1, 0)
    },
    decrementYear() {
      this.bike_form_object.year = FormUtils
        .decrementNumber(this.bike_form_object.year, 1, 0)
    },
    addSetupRow() {
      this.bike_form_object.setup_individual.push(_.clone(this.setup_individual_object, true));
    }
  },
  updated() {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
