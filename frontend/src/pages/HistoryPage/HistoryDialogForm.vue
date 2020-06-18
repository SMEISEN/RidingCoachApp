<template>
  <v-dialog
    v-model="maintenance_dialog"
    persistent max-width="500px"
    ref="addMaintenanceDialog"
  >
    <v-form
      v-model="valid"
      ref="validation_form"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add maintenance entry</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="auto" xs="12" sm="8" md="8">
              <v-menu
                ref="date_menu"
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
                    v-model="history_form_input.date"
                    prepend-icon="mdi-calendar"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="history_form_input.date"
                  @input=
                    "$emit('update:history_form_input', history_form_input); date_menu = false;"
                >
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="auto" xs="12" sm="4" md="4">
              <v-menu
                ref="time_menu"
                v-model="time_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="history_form_input.time"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="history_form_input.time"
                    prepend-icon="mdi-clock"
                    append-outer-icon="mdi-update"
                    @click:append-outer.prevent="refreshDateTime"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker
                  v-if="time_menu"
                  v-model="history_form_input.time"
                  format="24hr"
                  scrollable
                  full-width
                  @click:minute="$refs.time_menu.save(history_form_input.time)"
                ></v-time-picker>
              </v-menu>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12" xs="12" sm="8" md="8">
              <v-select
                v-model="history_form_input.category"
                :items="maintenance_categories"
                :rules="[v => !!v]"
                label="Category name*"
                required
                @select="$emit('update:history_form_input', history_form_input);"
              ></v-select>
            </v-col>
            <v-col cols="12" xs="12" sm="4" md="4">
              <v-text-field
                v-model="history_form_input.operating_hours"
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                @click:append-outer.prevent="increment"
                @click:prepend.prevent="decrement"
                :rules="[v => !!v]"
                required
                hint="of engine operation"
                suffix="h*"
                @keydown="$emit('update:history_form_input', history_form_input);"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-combobox
                v-model="history_form_input.name"
                :items="getMaintenanceNamesFromCategory(history_form_input.category)"
                :rules="[v => !!v]"
                label="Maintenance*"
                required
                ref="NameComboBox"
                @keydown="$emit('update:history_form_input', history_form_input);"
              ></v-combobox>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-text-field
                v-model="history_form_input.comment"
                label="Comment"
                @keydown="$emit('update:history_form_input', history_form_input);"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-spacer></v-spacer>
          <p class="text--secondary text-sm-right">
            *indicates required field</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="secondary"
            text
            @click.prevent="onCancel"
          >Close</v-btn>
          <v-btn
            color="secondary"
            :disabled="!valid"
            text
            @click.prevent="onSave"
          >Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import {HistoryApi} from '../../components/common/HistoryApi';


export default {
  name: 'HistoryForm',
  props: {
    history_form_input: {
      type: Object,
      required: true,
    },
    maintenance_categories: {
      type: Array,
      required: true,
    },
    maintenance_names: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    date_menu: false,
    time_menu: false,
    valid: true,
  }),
  computed: {
    maintenance_dialog: {
      get() { return this.$store.getters.getHistoryAddOrEditDialog },
      set(value) { this.$store.commit('setHistoryAddOrEditDialog', value) }
    },
  },
  methods: {
    getMaintenanceNamesFromCategory(category) {
      if (this.maintenance_categories.includes(category)) {
        return Object.keys(this.maintenance_names[category]);
      } return [];
    },
    initForm() {
      Object.keys(this.history_form_input).forEach((index) => {
        this.history_form_input[index] = null;
      });
      this.history_form_input.date = new Date().toISOString().substr(0, 10);
      this.history_form_input.time = new Date().toTimeString().substr(0, 5);
      this.history_form_input.operating_hours = this.$store.getters.getCurrentBikeOperatingHours;
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
      this.$store.commit('setHistoryEditFlag', false);
    },
    refreshDateTime() {
      this.history_form_input.date = new Date().toISOString().substr(0, 10);
      this.history_form_input.time = new Date().toTimeString().substr(0, 5);
      this.$forceUpdate();
    },
    increment() {
      this.history_form_input.operating_hours = Number(
        parseFloat(this.history_form_input.operating_hours) + 0.1,
      ).toFixed(1);
    },
    decrement() {
      this.history_form_input.operating_hours = Number(
        parseFloat(this.history_form_input.operating_hours) - 0.1,
      ).toFixed(1);
    },
    onSave() {
      this.$refs.NameComboBox.blur();
      this.$nextTick(() => {
        const datetime = this.history_form_input.date.concat('T', this.history_form_input.time);
        const payload = {
          maintenance_id:
          this.maintenance_names[
            this.history_form_input.category][
            this.history_form_input.name].maintenance_id,
          bike_id: this.$store.getters.getCurrentBikeId,
          operating_hours: this.history_form_input.operating_hours,
          datetime_display: Date.parse(datetime),
          comment: this.history_form_input.comment,
        };
        if (this.$store.getters.getHistoryEditFlag === false) {
          HistoryApi.postHistory(payload).then(() => {
            this.$emit('saveButtonClicked')
            this.$store.commit('setHistoryAddOrEditDialog', false);
            this.initForm();
          });
        } else {
          const HistId = this.history_form_input.history_id;
          HistoryApi.putHistoryItem(payload, HistId).then(() => {
            this.$emit('saveButtonClicked')
            this.$store.commit('setHistoryAddOrEditDialog', false);
            this.initForm();
          });
        }
      });
    },
    onCancel() {
      this.$emit('cancelButtonClicked');
      this.$store.commit('setHistoryAddOrEditDialog', false);
      this.initForm();
    },
  },
  created() {
  },
  updated() {
  }
}
</script>

<style scoped>

</style>
