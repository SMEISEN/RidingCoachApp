<template>
  <v-dialog
    ref="addMaintenanceDialog"
    v-model="maintenance_dialog"
    persistent
    max-width="500px"
  >
    <v-form
      v-if="maintenance_dialog"
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add maintenance entry</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="8"
              md="8"
            >
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
                    v-model="historyFormInput.date"
                    prepend-icon="mdi-calendar"
                    :rules="[v => !!v]"
                    readonly
                    required
                    v-on="on"
                  />
                </template>
                <v-date-picker
                  v-model="historyFormInput.date"
                  @input="date_menu = false"
                />
              </v-menu>
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="4"
              md="4"
            >
              <v-menu
                ref="time_menu"
                v-model="time_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="historyFormInput.time"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="historyFormInput.time"
                    prepend-icon="mdi-clock"
                    append-outer-icon="mdi-update"
                    :rules="[v => !!v]"
                    readonly
                    required
                    @click:append-outer.prevent="refreshDateTime"
                    v-on="on"
                  />
                </template>
                <v-time-picker
                  v-if="time_menu"
                  v-model="historyFormInput.time"
                  format="24hr"
                  scrollable
                  full-width
                  @click:minute="$refs.time_menu.save(historyFormInput.time)"
                />
              </v-menu>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col
              cols="12"
              xs="12"
              sm="8"
              md="8"
            >
              <v-select
                v-model="historyFormInput.category"
                :items="maintenanceCategories"
                :rules="[v => !!v]"
                label="Category name*"
                required
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="4"
              md="4"
            >
              <v-text-field
                v-model.number="historyFormInput.operating_hours"
                append-outer-icon="mdi-plus"
                prepend-icon="mdi-minus"
                :rules="[v => !!v]"
                required
                hint="of engine operation"
                suffix="h*"
                @click:append-outer.prevent="increment"
                @click:prepend.prevent="decrement"
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-combobox
                ref="NameComboBox"
                v-model="historyFormInput.name"
                :items="getMaintenanceNamesFromCategory(historyFormInput.category)"
                :rules="[v => !!v]"
                label="Maintenance*"
                required
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-select
              v-model="historyFormInput.tags"
              :items="maintenanceTags"
              :rules="[v => !!v]"
              label="Tags"
              chips
              multiple
            >
              <template v-slot:selection="{ attrs, item, select, selected }">
                <v-chip
                  v-bind="attrs"
                  :input-value="selected"
                  :color="chipColor(item)"
                  close
                  outlined
                  @click="select"
                  @click:close="removeTagChips(item)"
                >
                  <v-icon
                    v-if="item === 'checked'"
                    left
                  >
                    mdi-check-circle-outline
                  </v-icon>
                  <v-icon
                    v-if="item === 'fixed'"
                    left
                  >
                    mdi-progress-wrench
                  </v-icon>
                  <v-icon
                    v-if="item === 'replaced'"
                    left
                  >
                    mdi-refresh
                  </v-icon>
                  <span>{{ item }}</span>
                </v-chip>
              </template>
            </v-select>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <v-text-field
                v-model="historyFormInput.comment"
                label="Comment"
              />
            </v-col>
          </v-row>
          <v-spacer />
          <p class="text--secondary text-sm-right">
            *indicates required field
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            text
            @click.prevent="onCancel"
          >
            Close
          </v-btn>
          <v-btn
            color="secondary"
            :disabled="!valid"
            text
            @click.prevent="onSave"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import {
  apiPostHistory,
  apiPutHistoryItem,
} from '../../components/api/HistoryApi';
import {
  initObject,
  incrementNumber,
  decrementNumber,
} from '../../components/utils/FromUtils';
import { apiPostMaintenance } from '../../components/api/MaintenanceApi';

export default {
  name: 'HistoryForm',
  props: {
    historyFormInput: {
      type: Object,
      required: true,
    },
    maintenanceCategories: {
      type: Array,
      required: true,
    },
    maintenanceNames: {
      type: Object,
      required: true,
    },
    maintenanceTags: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    date_menu: false,
    time_menu: false,
    valid: true,
    changed: false,
  }),
  computed: {
    maintenance_dialog: {
      get() {
        return this.$store.getters.getHistoryAddOrEditDialog;
      },
      set(value) {
        this.$store.commit('setHistoryAddOrEditDialog', value);
      },
    },
    maintenance_name() {
      return this.historyFormInput.name;
    },
  },
  watch: {
    maintenance_name() {
      const { category } = this.historyFormInput;
      const { name } = this.historyFormInput;
      if (category !== null) {
        if (name !== null) {
          if (this.$store.getters.getHistoryEditFlag === false) {
            this.historyFormInput.tags = this.getDefaultTags(category, name);
          }
          if (this.changed === false) {
            this.changed = true;
          } else {
            this.historyFormInput.tags = this.getDefaultTags(category, name);
          }
        }
      }
    },
  },
  created() {
  },
  updated() {
  },
  methods: {
    chipColor(item) {
      if (item === 'checked') {
        return 'success';
      }
      if (item === 'fixed') {
        return 'warning';
      }
      if (item === 'replaced') {
        return 'error';
      }
      return 'grey';
    },
    removeTagChips(item) {
      this.historyFormInput.tags.splice(this.historyFormInput.tags.indexOf(item), 1);
      this.historyFormInput.tags = [...this.historyFormInput.tags];
    },
    getMaintenanceNamesFromCategory(category) {
      if (this.maintenanceCategories.includes(category)) {
        return Object.keys(this.maintenanceNames[category]);
      } return [];
    },
    getDefaultTags(category, name) {
      if (this.maintenanceCategories.includes(category)) {
        if (Object.keys(this.maintenanceNames[category]).includes(name)) {
          return this.maintenanceNames[category][name].tags_default;
        }
      }
      return [];
    },
    initForm() {
      initObject(this.historyFormInput, null);
      this.historyFormInput.date = new Date().toISOString().substr(0, 10);
      this.historyFormInput.time = new Date().toTimeString().substr(0, 5);
      this.historyFormInput.operating_hours = this.$store.getters.getCurrentBikeOperatingHours;
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
      this.$store.commit('setHistoryEditFlag', false);
      this.changed = false;
    },
    refreshDateTime() {
      this.historyFormInput.date = new Date().toISOString().substr(0, 10);
      this.historyFormInput.time = new Date().toTimeString().substr(0, 5);
      this.$forceUpdate();
    },
    increment() {
      this.historyFormInput.operating_hours = incrementNumber(
        this.historyFormInput.operating_hours, 0.1, 1,
      );
    },
    decrement() {
      this.historyFormInput.operating_hours = decrementNumber(
        this.historyFormInput.operating_hours, 0.1, 1,
      );
    },
    onSave() {
      this.$refs.NameComboBox.blur();
      this.$nextTick(() => {
        const datetime = this.historyFormInput.date.concat('T', this.historyFormInput.time);
        const histPayload = {
          bike_id: this.$store.getters.getCurrentBikeId,
          operating_hours: this.historyFormInput.operating_hours,
          datetime_display: Date.parse(datetime) / 1000,
          tags: this.historyFormInput.tags,
          comment: this.historyFormInput.comment,
        };
        if (Object.keys(this.maintenanceNames[this.historyFormInput.category])
          .includes(this.historyFormInput.name)) {
          histPayload.maintenance_id = this.maintenanceNames[
            this.historyFormInput.category][
            this.historyFormInput.name].maintenance_id;
          this.pushHistory(histPayload);
        } else {
          const mtnPayload = {
            category: this.historyFormInput.category,
            name: this.historyFormInput.name,
            interval_type: 'unplanned cycle',
          };
          apiPostMaintenance(mtnPayload)
            .then((res) => {
              histPayload.maintenance_id = res.data;
              this.pushHistory(histPayload);
            })
            .catch((error) => {
              this.$store.commit('setInfoSnackbar', {
                state: true,
                color: 'error',
                message: `${error}!`,
              });
            });
        }
      });
    },
    pushHistory(payload) {
      if (this.$store.getters.getHistoryEditFlag === false) {
        apiPostHistory(payload)
          .then(() => {
            this.$emit('saveButtonClicked');
            this.maintenance_dialog = false;
            this.initForm();
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'success',
              message: 'Maintenance history entry added!',
            });
          })
          .catch((error) => {
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
          });
      } else {
        const HistId = this.historyFormInput.history_id;
        apiPutHistoryItem(payload, HistId)
          .then(() => {
            this.$emit('saveButtonClicked');
            this.maintenance_dialog = false;
            this.initForm();
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'success',
              message: 'Maintenance history entry edited!',
            });
          })
          .catch((error) => {
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
          });
      }
    },
    onCancel() {
      this.$emit('cancelButtonClicked');
      this.maintenance_dialog = false;
      this.initForm();
    },
  },
};
</script>

<style scoped>

</style>
