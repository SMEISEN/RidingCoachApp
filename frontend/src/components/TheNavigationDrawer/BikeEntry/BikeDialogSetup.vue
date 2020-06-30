<template>
  <div>
    <v-subheader>Available setup</v-subheader>
    <v-card-text>
      <v-simple-table dense>
        <thead>
          <tr>
            <th class="text-left">
              Category
            </th>
            <th class="text-left">
              Group
            </th>
            <th class="text-left">
              Name
            </th>
            <th class="text-left">
              Available ticks
            </th>
            <th class="text-left">
              Standard tick
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(entry, index) in setupIndividual"
            :key="index"
          >
            <td style="border-bottom: none">
              <v-select
                v-model="entry.category"
                :items="['Engine', 'Suspension', 'Electronic']"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.group"
                style="font-size: 12px"
                dense
                height="20px"
                placeholder="default"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.name"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.ticks_available"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.ticks_standard"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
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
    bikeFormObject: {
      type: Object,
      required: true,
    },
    setupIndividual: {
      type: Array,
      required: true,
    },
    setupIndividualTemplate: {
      type: Object,
      required: true,
    },
  },
  updated() {
  },
  created() {
  },
  methods: {
    addSetupRow() {
      this.bikeFormObject.setup_individual.push(this._.cloneDeep(this.setupIndividualTemplate));
    },
  },
};
</script>

<style scoped>

</style>
