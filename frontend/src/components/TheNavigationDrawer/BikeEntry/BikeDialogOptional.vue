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
            v-model="bikeFormObject.ccm"
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
            v-model="bikeFormObject.stroke"
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
            v-model="bikeFormObject.piston"
            label="Engine piston"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-text-field
            v-model="bikeFormObject.slick_front"
            label="Slick front"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-text-field
            v-model="bikeFormObject.slick_rear"
            label="Slick rear"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-text-field
            v-model="bikeFormObject.rain_front"
            label="Rain front"
          />
        </v-col>
        <v-col
          cols="12"
          xs="12"
          sm="6"
          md="6"
        >
          <v-text-field
            v-model="bikeFormObject.rain_rear"
            label="Rain rear"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </div>
</template>

<script>
export default {
  name: 'BikeDialogOptional',
  props: {
    bikeFormObject: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
