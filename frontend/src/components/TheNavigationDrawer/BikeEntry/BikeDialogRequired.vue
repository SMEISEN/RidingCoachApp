<template>
  <div>
    <v-subheader>Required fields</v-subheader>
    <v-card-text>
      <v-row dense>
        <v-col
          cols="12"
          xs="12"
          sm="4"
          md="4"
        >
          <v-text-field
            v-model="bikeFormObject.manufacturer"
            label="Manufacturer*"
            :rules="[v => !!v]"
            required
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="5"
          md="6"
        >
          <v-text-field
            v-model="bikeFormObject.model"
            label="Model*"
            :rules="[v => !!v]"
            required
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="3"
          md="2"
        >
          <v-text-field
            v-model.number="bikeFormObject.year"
            :rules="[v => !!v]"
            required
            label="Year*"
            append-outer-icon="mdi-plus"
            prepend-icon="mdi-minus"
            @click:append-outer="incrementYear"
            @click:prepend="decrementYear"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="9"
          md="10"
        />
        <v-col
          cols="12"
          xs="12"
          sm="3"
          md="2"
        >
          <v-text-field
            v-model.number="bikeFormObject.operating_hours"
            :rules="[v => !!v]"
            required
            label="Operating hours*"
            hint="of engine"
            suffix="h"
            append-outer-icon="mdi-plus"
            prepend-icon="mdi-minus"
            @click:append-outer="incrementHour"
            @click:prepend="decrementHour"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </div>
</template>

<script>
import {
  incrementNumber,
  decrementNumber,
} from '../../utils/FromUtils';

export default {
  name: 'BikeDialogRequired',
  props: {
    bikeFormObject: {
      type: Object,
      required: true,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    incrementHour() {
      this.bikeFormObject.operating_hours = incrementNumber(
        this.bikeFormObject.operating_hours, 0.1, 1,
      );
    },
    decrementHour() {
      this.bikeFormObject.operating_hours = decrementNumber(
        this.bikeFormObject.operating_hours, 0.1, 1,
      );
    },
    incrementYear() {
      this.bikeFormObject.year = incrementNumber(
        this.bikeFormObject.year, 1, 0,
      );
    },
    decrementYear() {
      this.bikeFormObject.year = decrementNumber(
        this.bikeFormObject.year, 1, 0,
      );
    },
  },
};
</script>

<style scoped>

</style>
