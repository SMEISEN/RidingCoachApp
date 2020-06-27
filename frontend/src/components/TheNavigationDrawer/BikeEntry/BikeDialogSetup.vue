<template>
  <div>
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
        <tr v-for="(entry, index) in setup_individual"
            v-bind:key="index">
          <td style="border-bottom: none"><v-select
            :items="['Engine', 'Suspension', 'Electronic']"
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
  </div>
</template>

<script>
export default {
  name: 'BikeDialogSetup',
  props: {
    bike_form_object: {
      type: Object,
      required: true,
    },
    setup_individual: {
      type: Array,
      required: true,
    },
    setup_individual_template: {
      type: Object,
      required: true,
    },
  },
  methods: {
    addSetupRow() {
      this.bike_form_object.setup_individual.push(_.clone(this.setup_individual_template, true));
    }
  }
}
</script>

<style scoped>

</style>
