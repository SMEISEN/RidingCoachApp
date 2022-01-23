<template>
  <v-dialog
    v-model="tire_dialog"
    persistent
    max-width="500px"
  >
    <v-form
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">{{ task }} tire</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="6"
            >
              <v-select
                v-model="tire_data_object.category"
                :items="category_array"
                :rules="[v => !!v]"
                label="Category*"
                required
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="6"
            >
              <v-select
                v-model="tire_data_object.axis"
                :items="axis_array"
                :rules="[v => !!v]"
                label="Axis*"
                required
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model="tire_data_object.manufacturer"
                :rules="[v => !!v]"
                label="Manufacturer*"
                required
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model="tire_data_object.name"
                label="Name"
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model="tire_data_object.dimension"
                label="Dimension"
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="4"
              sm="4"
              md="4"
            >
              <v-text-field
                v-model="tire_data_object.compound"
                label="Compound"
              />
            </v-col>
            <v-col
              cols="12"
              xs="4"
              sm="4"
              md="4"
            >
              <v-text-field
                v-model="tire_data_object.dot"
                :rules="[v => !!v]"
                label="DOT*"
                required
              />
            </v-col>
            <v-col
              cols="12"
              xs="4"
              sm="4"
              md="4"
            >
              <v-text-field
                v-model.number="tire_data_object.operating_hours"
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                :rules="[v => !!v]"
                required
                hint="of engine operation"
                suffix="h*"
                @click:append-outer.prevent="increment"
                @click:prepend.prevent="decrement"
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col cols="12">
              <v-text-field
                v-model="tire_data_object.comment"
                label="Comment"
              />
            </v-col>
          </v-row>
          <v-spacer />
          <v-row>
            <v-col cols="12">
              <span>Tire condition</span>
            </v-col>
          </v-row>
          <v-spacer />
          <v-row>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-slider
                  v-model.number="tire_data_object.condition.left_outer"
                  vertical
                  hide-details
                  thumb-label
                  v-bind="attrs"
                  max="1"
                  min="0"
                  step="0.01"
                  color="black"
                  track-color="neutral"
                  prepend-icon="mdi-arrow-left-drop-circle"
                  v-on="on"
                >
                  <template v-slot:thumb-label="{ value }">
                    {{ parseInt(value * 100) }}
                  </template>
                </v-slider>
              </template>
              <span>Outer left</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-slider
                  v-model="tire_data_object.condition.left_middle"
                  vertical
                  hide-details
                  thumb-label
                  v-bind="attrs"
                  max="1"
                  min="0"
                  step="0.01"
                  color="black"
                  track-color="neutral"
                  v-on="on"
                >
                  <template v-slot:thumb-label="{ value }">
                    {{ parseInt(value * 100) }}
                  </template>
                </v-slider>
              </template>
              <span>Middle left</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-slider
                  v-model="tire_data_object.condition.center"
                  vertical
                  hide-details
                  thumb-label
                  v-bind="attrs"
                  max="1"
                  min="0"
                  step="0.01"
                  color="black"
                  track-color="neutral"
                  prepend-icon="mdi-record-circle"
                  v-on="on"
                >
                  <template v-slot:thumb-label="{ value }">
                    {{ parseInt(value * 100) }}
                  </template>
                </v-slider>
              </template>
              <span>Center</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-slider
                  v-model="tire_data_object.condition.right_middle"
                  vertical
                  hide-details
                  thumb-label
                  v-bind="attrs"
                  max="1"
                  min="0"
                  step="0.01"
                  color="black"
                  track-color="neutral"
                  v-on="on"
                >
                  <template v-slot:thumb-label="{ value }">
                    {{ parseInt(value * 100) }}
                  </template>
                </v-slider>
              </template>
              <span>Middle right</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-slider
                  v-model="tire_data_object.condition.right_outer"
                  vertical
                  hide-details
                  thumb-label
                  v-bind="attrs"
                  max="1"
                  min="0"
                  step="0.01"
                  color="black"
                  track-color="neutral"
                  prepend-icon="mdi-arrow-right-drop-circle"
                  v-on="on"
                >
                  <template v-slot:thumb-label="{ value }">
                    {{ parseInt(value * 100) }}
                  </template>
                </v-slider>
              </template>
              <span>Outer right</span>
            </v-tooltip>
          </v-row>
          <v-spacer />
          <p class="text--secondary text-sm-right">
            *indicates required field
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            text
            @click.prevent="onCancel"
          >
            Close
          </v-btn>
          <v-btn
            color="secondary"
            :disabled="!valid"
            text
            @click.prevent="onSave"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import {
  apiPostTire,
  apiPutTireItem,
} from '../../api/TireApi';
import {
  incrementNumber,
  decrementNumber,
} from '../../utils/FromUtils';

export default {
  name: 'TireDialogTabsExpansionDialog',
  components: {
  },
  props: {
    tireDialog: {
      type: Boolean,
      required: true,
    },
    task: {
      type: String,
      required: true,
    },
    tireDataObject: {
      type: Object,
      required: true,
    },
    tireArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    valid: true,
    category_array: [
      'Slick',
      'Rain',
    ],
    axis_array: [
      'Front',
      'Rear',
    ],
  }),
  computed: {
    tire_data_object: {
      get() {
        return this.tireDataObject;
      },
      set(value) {
        this.$emit('update:tireDataObject', value);
      },
    },
    tire_dialog: {
      get() {
        return this.tireDialog;
      },
      set(value) {
        this.$emit('update:tireDialog', value);
      },
    },
    tire_array() {
      return this.tireArray;
    },
  },
  methods: {
    /**
     * Resets the validation of the dialog form in the tire expander.
     */
    resetValidation() {
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
    },
    /**
     * Depending on task, add a new tire to the database or modify an existing one.
     */
    onSave() {
      const payload = this.tire_data_object;
      const tireId = this.tire_data_object.tire_id;
      if (this.task === 'Add') {
        apiPostTire(payload).then((res) => {
          this.tire_data_object.tire_id = res.data;
          this.$emit('refreshTires');
          this.$emit('resetTireForm');
          this.tire_dialog = false;
        });
      } else {
        apiPutTireItem(payload, tireId).then(() => {
          this.$emit('refreshTires');
          this.$emit('resetTireForm');
          this.tire_dialog = false;
        });
      }
      this.resetValidation();
    },
    /**
     * Resets the validation of the dialog form in the tire expander and closes the tire dialog.
     */
    onCancel() {
      this.resetValidation();
      this.$emit('resetTireForm');
      this.tire_dialog = false;
    },
    /**
     * Increases the operating hours of a tire by 0.1 h.
     */
    increment() {
      this.tire_data_object.operating_hours = incrementNumber(
        this.tire_data_object.operating_hours, 0.1, 1,
      );
    },
    /**
     * Decreases the operating hours of a tire by 0.1 h.
     */
    decrement() {
      this.tire_data_object.operating_hours = decrementNumber(
        this.tire_data_object.operating_hours, 0.1, 1,
      );
    },
  },
};
</script>
