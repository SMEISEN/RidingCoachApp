<template>
  <div>
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
  </div>
</template>

<script>
import {FormUtils} from '../../utils/FromUtils';

export default {
  name: 'BikeDialogRequired',
  props: {
    bike_form_object: {
      type: Object,
      required: true,
    },
  },
  methods: {
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
  }
}
</script>

<style scoped>

</style>
