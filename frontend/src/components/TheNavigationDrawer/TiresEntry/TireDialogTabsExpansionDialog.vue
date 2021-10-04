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
  apiPutTireItem
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
  data: () => ({
    valid: true,
    category_array: [
      'Slick',
      'Rain'
    ],
    axis_array: [
      'Front',
      'Rear',
    ],
  }),
  methods: {
    addTire() {
    },
    resetValidation() {
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
    },
    onSave() {
      const payload = this.tire_data_object;
      const tire_id = this.tire_data_object.tire_id;
      if (this.task == 'Add') {
        apiPostTire(payload).then((res) => {
          this.tire_data_object.tire_id = res.data;
          this.$emit('refreshTires');
          this.$emit('resetTireForm');
          this.tire_dialog = false;
        });
      } else {
        apiPutTireItem(payload, tire_id).then((res) => {
          this.$emit('refreshTires');
          this.$emit('resetTireForm');
          this.tire_dialog = false;
        });
      }
      this.resetValidation();
    },
    onCancel() {
      this.resetValidation();
      this.$emit('resetTireForm');
      this.tire_dialog = false;
    },
    increment() {
      this.tire_data_object.operating_hours = incrementNumber(
        this.tire_data_object.operating_hours, 0.1, 1,
      );
    },
    decrement() {
      this.tire_data_object.operating_hours = decrementNumber(
        this.tire_data_object.operating_hours, 0.1, 1,
      );
    },
  },
};
</script>

<style scoped>

</style>