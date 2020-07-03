<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Location</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row>
        <v-col
          cols="12"
          xs="12"
          sm="9"
          md="10"
          class="px-6"
        >
          <v-combobox
            v-model="trainingFormObject.race_track"
            label="Race track*"
            :rules="[v => !!v]"
            required
          />
        </v-col>
        <v-col
          cols="auto"
          xs="12"
          sm="3"
          md="2"
          class="px-6"
        >
          <v-menu
            v-model="date_menu"
            :close-on-content-click="false"
            :nudge-right="40"
            scrollable
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field
                v-model="trainingFormObject.date"
                prepend-icon="mdi-calendar"
                required
                v-on="on"
              />
            </template>
            <v-date-picker
              v-model="trainingFormObject.date"
              @input="date_menu = false"
            />
          </v-menu>
        </v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: 'TrainingDialogGeneralLocation',
  props: {
    trainingFormObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    date_menu: false,
  }),
};
</script>

<style scoped>

</style>
