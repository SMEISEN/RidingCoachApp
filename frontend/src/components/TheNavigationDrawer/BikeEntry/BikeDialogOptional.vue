<template>
  <div>
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
  </div>
</template>

<script>
export default {
  name: 'BikeDialogOptional',
  props: {
    bike_form_object: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style scoped>

</style>
