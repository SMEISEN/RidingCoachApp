<template v-slot:default>
  <v-app>
    <v-flex>
      <v-layout wrap>
        <v-container>
          <v-card class="card-container">
            <v-card-title>
              <v-btn color="secondary" dark
                     @click="maintenance_dialog = true">Add maintenance entry
              </v-btn>
            </v-card-title>
            <v-simple-table fixed-header height="500px">
              <thead>
              <tr>
                <th class="text-left">Category</th>
                <th class="text-left" style="min-width: 120px">Name</th>
                <th class="text-left">Hours</th>
                <th class="text-left">Date</th>
                <th class="text-left">Comment</th>
                <th></th>
              </tr>
              </thead>
              <tbody>
                <tr v-for="(maintenance) in history_list"
                    v-bind:key="maintenance.history_id"
                    v-bind:MtnId="maintenance.history_id">
                  <td style="font-size: 12px">{{ maintenance.category }}</td>
                  <td style="font-size: 12px">{{ maintenance.name }}</td>
                  <td>{{ maintenance.operating_hours }}</td>
                  <td>{{ maintenance.datetime_display | formatDateTime }}</td>
                  <td>{{ maintenance.comment }}</td>
                  <td>
                    <div class="btn-group" role="group">
                      <v-btn color="warning" text @click="editHistory(maintenance.history_id)">
                        Edit
                      </v-btn>
                      <v-btn color="error" text @click="deleteHistory(maintenance.history_id)">
                        Delete
                      </v-btn>
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-container>
      </v-layout>
    </v-flex>
    <v-dialog v-model="maintenance_dialog"
              persistent max-width="500px"
              ref="addMaintenanceDialog"
              @keydown.esc="maintenance_dialog = false"
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
            <v-row no-gutters>
              <v-col cols="auto" xs="12" sm="8" md="8">
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
                      v-model="history_form_dict.date"
                      prepend-icon="mdi-calendar"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="history_form_dict.date"
                                 @input="date_menu = false">
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="auto" xs="12" sm="4" md="4">
                <v-menu
                  ref="menu"
                  v-model="time_menu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="history_form_dict.time"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="history_form_dict.time"
                      prepend-icon="mdi-clock"
                      append-outer-icon="mdi-update"
                      @click:append-outer="refreshDateTime"
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-if="time_menu"
                    v-model="history_form_dict.time"
                    format="24hr"
                    scrollable
                    full-width
                    @click:minute="$refs.menu.save(history_form_dict.time)"
                  ></v-time-picker>
                </v-menu>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col cols="12" xs="12" sm="8" md="8">
                <v-select :items="maintenance_categories_list"
                          :rules="[v => !!v]"
                          label="Category name*"
                          required
                          v-model="history_form_dict.category">
                </v-select>
              </v-col>
              <v-col cols="12" xs="12" sm="4" md="4">
                <v-text-field
                  append-outer-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  @click:append-outer="increment"
                  @click:prepend="decrement"
                  :rules="[v => !!v]"
                  required
                  hint="of engine operation"
                  suffix="h*"
                  v-model="history_form_dict.operating_hours">
                </v-text-field>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col cols="12">
                <v-combobox
                  :items="getMaintenanceNamesFromCategory(history_form_dict.category)"
                  :rules="[v => !!v]"
                  label="Maintenance*"
                  required
                  ref="NameComboBox"
                  v-model="history_form_dict.name">
                </v-combobox>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col cols="12">
                <v-text-field label="Comment"
                              v-model="history_form_dict.comment">
                </v-text-field>
              </v-col>
            </v-row>
            <v-spacer></v-spacer>
            <p class="text--secondary text-sm-right">
              *indicates required field</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" text @click="onCancel">Close</v-btn>
            <v-btn color="secondary" :disabled="!valid"
                   text @click="onSubmit">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
    <v-dialog v-model="confirm_delete_dialog" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">
          Warning
        </v-card-title>
        <v-card-text>
          <p class="text--primary">
            Do you really want to delete this maintenance entry?</p>
          <p class="text--secondary text-sm-left">
            The deletion is permanent and cannot be undone.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="accent" text
                 @click="confirm_delete_dialog = false">Cancel</v-btn>
          <v-btn color="error" text
                 @click="deleteHistoryItem()">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'History',
  metaInfo: {
    title: 'History',
  },
  data: () => ({
    history_list: [],
    history_form_dict: {
      history_id: '',
      maintenance_id: '',
      category: '',
      name: '',
      operating_hours: '',
      date: new Date().toISOString().substr(0, 10),
      time: new Date().toTimeString().substr(0, 5),
      comment: '',
    },
    maintenance_categories_list: [],
    maintenance_names_dict: {},
    edit: false,
    maintenance_dialog: false,
    confirm_delete_dialog: false,
    date_menu: false,
    time_menu: false,
    valid: true,
  }),
  methods: {
    getMaintenanceNamesFromCategory(category) {
      if (this.maintenance_categories_list.includes(category)) {
        return Object.keys(this.maintenance_names_dict[category]);
      } return [];
    },
    getHistory() {
      const ApiPath = '/api/history/query';
      const payload = {
        bike_id: this.$store.getters.getCurrentBikeId,
      };
      axios.post(ApiPath, payload)
        .then((res) => {
          this.history_list = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    postHistory(payload) {
      const ApiPath = '/api/history';
      axios.post(ApiPath, payload)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.error(error);
          this.getHistory();
        });
    },
    getMaintenanceCategoriesAndNames() {
      const ApiPath = '/api/maintenance';
      axios.get(ApiPath)
        .then((res) => {
          this.maintenance_categories_list = Object.keys(res.data);
          this.maintenance_names_dict = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    initForm() {
      this.history_form_dict.history_id = '';
      this.history_form_dict.category = '';
      this.history_form_dict.name = '';
      this.history_form_dict.date = new Date().toISOString().substr(0, 10);
      this.history_form_dict.time = new Date().toTimeString().substr(0, 5);
      this.history_form_dict.operating_hours = this.$store.getters.getCurrentBikeOperatingHours;
      this.history_form_dict.comment = '';
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
      this.edit = false;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.NameComboBox.blur();
      this.$nextTick(() => {
        const datetime = this.history_form_dict.date.concat('T', this.history_form_dict.time);
        const payload = {
          maintenance_id:
            this.maintenance_names_dict[
              this.history_form_dict.category][
              this.history_form_dict.name].maintenance_id,
          bike_id: this.$store.getters.getCurrentBikeId,
          operating_hours: this.history_form_dict.operating_hours,
          datetime_display: Date.parse(datetime),
          comment: this.history_form_dict.comment,
        };
        if (this.edit === false) {
          this.postHistory(payload);
        } else {
          this.putHistoryItem(payload);
        }
        this.maintenance_dialog = false;
        this.initForm();
      });
    },
    onCancel(evt) {
      evt.preventDefault();
      this.maintenance_dialog = false;
      this.initForm();
    },
    increment() {
      this.history_form_dict.operating_hours = Number(
        parseFloat(this.history_form_dict.operating_hours) + 0.1,
      ).toFixed(1);
    },
    decrement() {
      this.history_form_dict.operating_hours = Number(
        parseFloat(this.history_form_dict.operating_hours) - 0.1,
      ).toFixed(1);
    },
    editHistory(HistId) {
      const ApiPath = `/api/history/${HistId}`;
      axios.get(ApiPath)
        .then((res) => {
          this.history_form_dict.history_id = res.data.history_id;
          this.history_form_dict.maintenance_id = res.data.maintenance_id;
          this.history_form_dict.category = res.data.category;
          this.history_form_dict.name = res.data.name;
          this.history_form_dict.operating_hours = res.data.operating_hours;
          this.history_form_dict.date = this.$options.filters
            .formatDateTime(res.data.datetime_display).substring(0, 10);
          this.history_form_dict.time = this.$options.filters
            .formatDateTime(res.data.datetime_display).substring(11, 16);
          this.history_form_dict.comment = res.data.comment;
        })
        .catch((error) => {
          console.error(error);
        });
      this.edit = true;
      this.maintenance_dialog = true;
    },
    putHistoryItem(payload) {
      const ApiPath = `/api/history/${this.history_form_dict.history_id}`;
      axios.put(ApiPath, payload)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.error(error);
          this.getHistory();
        });
      this.edit = false;
    },
    deleteHistory(HistId) {
      this.confirm_delete_dialog = true;
      this.history_form_dict.history_id = HistId;
    },
    deleteHistoryItem() {
      const ApiPath = `/api/history/${this.history_form_dict.history_id}`;
      axios.delete(ApiPath)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.error(error);
          this.getHistory();
        });
      this.confirm_delete_dialog = false;
    },
    refreshDateTime() {
      this.history_form_dict.date = new Date().toISOString().substr(0, 10);
      this.history_form_dict.time = new Date().toTimeString().substr(0, 5);
    },
  },
  created() {
    this.getHistory();
    this.getMaintenanceCategoriesAndNames();
    this.initForm();
  },
  updated() {
  },
};
</script>
