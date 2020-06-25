<template>
  <v-dialog v-model="training_dialog" fullscreen hide-overlay
            transition="dialog-bottom-transition">
    <v-form
      v-model="valid_training_dialog"
      ref="validation_training_form"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click.prevent="onTrainingCancel()">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Training settings</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click.prevent="onTrainingSave()" :disabled="!valid_training_dialog">
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-card-text>
          <v-expansion-panels
            focusable
            v-model="training_general_panel"
          >
            <v-expansion-panel>
              <v-expansion-panel-header>Location</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-col cols="12" xs="12" sm="9" md="10">
                    <v-combobox
                      label="Race track*"
                      :rules="[v => !!v]"
                      required
                      v-model="training_form_object.race_track"
                    ></v-combobox>
                  </v-col>
                  <v-col cols="auto" xs="12" sm="3" md="2">
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
                          v-model="training_form_object.date"
                          prepend-icon="mdi-calendar"
                          required
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker v-model="training_form_object.date"
                                     @input="date_menu = false">
                      </v-date-picker>
                    </v-menu>
                  </v-col>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-header>Weather</v-expansion-panel-header>
              <v-expansion-panel-content>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
        <TheNavigationDrawerTrainingDialogTabs
          :training_form_object="training_form_object"
        />
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import TheNavigationDrawerTrainingDialogTabs from './TrainingDialogTabs';
export default {
  name: 'TheNavigationDrawerTrainingDialog',
  props: {
    training_form_object: {
      type: Object,
      required: true,
    },
  },
  components: {
    TheNavigationDrawerTrainingDialogTabs,
  },
  data: () => ({
    date_menu: false,
    training_general_panel: 0,
    valid_training_dialog: true,
  }),
  computed: {
    training_dialog: {
      get() {
        return this.$store.getters.getTrainingDialogState
      },
      set(value) {
        this.$store.commit('setTrainingDialogState', value)
      },
    },
  },
  methods: {
    onTrainingSave() {
      this.$emit('saveClicked');
    },
    onTrainingCancel() {
      this.training_dialog = false;
      this.training_setup_tabs = 1;
      this.training_setup_tab = null;
      this.$emit('cancelClicked');
    },
  },
}
</script>

<style scoped>

</style>
