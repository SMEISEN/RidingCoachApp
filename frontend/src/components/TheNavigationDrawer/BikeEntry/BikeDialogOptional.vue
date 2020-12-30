<template>
  <div>
    <v-subheader>Optional fields</v-subheader>
    <v-card-text>
      <v-row dense>
        <v-col
          cols="12"
          xs="4"
          sm="4"
          md="4"
        >
          <v-text-field
            v-model.number="bikeFormObject.ccm"
            label="Engine ccm"
          />
        </v-col>
        <v-col
          cols="12"
          xs="4"
          sm="4"
          md="4"
        >
          <v-text-field
            v-model.number="bikeFormObject.stroke"
            label="Engine stroke"
          />
        </v-col>
        <v-col
          cols="12"
          xs="4"
          sm="4"
          md="4"
        >
          <v-text-field
            v-model.number="bikeFormObject.piston"
            label="Engine piston"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="5"
          md="5"
        >
          <v-text-field
            v-model="bikeFormObject.slick_front_name"
            label="Slick tire front"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="1"
          md="1"
        >
          <BikeDialogTires
            :tire-pressure-array.sync="bikeFormObject.slick_front_pressure"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="5"
          md="5"
        >
          <v-text-field
            v-model="bikeFormObject.slick_rear_name"
            label="Slick tire rear"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="1"
          md="1"
        >
          <BikeDialogTires
            :tire-pressure-array.sync="bikeFormObject.slick_rear_pressure"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-textarea
            v-model="bikeFormObject.slick_front_notes"
            label="Slick tire front application notes"
            rows="1"
            auto-grow
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-textarea
            v-model="bikeFormObject.slick_rear_notes"
            label="Slick tire rear application notes"
            rows="1"
            auto-grow
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="5"
          md="5"
        >
          <v-text-field
            v-model="bikeFormObject.rain_front_name"
            label="Rain tire front"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="1"
          md="1"
        >
          <BikeDialogTires
            :tire-pressure-array.sync="bikeFormObject.rain_front_pressure"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="5"
          md="5"
        >
          <v-text-field
            v-model="bikeFormObject.rain_rear_name"
            label="Rain tire rear"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="1"
          md="1"
        >
          <BikeDialogTires
            :tire-pressure-array.sync="bikeFormObject.rain_rear_pressure"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-textarea
            v-model="bikeFormObject.rain_front_notes"
            label="Rain tire front application notes"
            rows="1"
            auto-grow
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-textarea
            v-model="bikeFormObject.rain_rear_notes"
            label="Rain tire rear application notes"
            rows="1"
            auto-grow
          />
        </v-col>
      </v-row>
    </v-card-text>
  </div>
</template>

<script>
import BikeDialogTires from './BikeDialogTires.vue';

export default {
  name: 'BikeDialogOptional',
  components: {
    BikeDialogTires,
  },
  props: {
    bikeFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    dialog: false,
    menu: false,
  }),
};
</script>

<style scoped>

</style>
