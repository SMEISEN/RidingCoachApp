<template v-slot:default>
  <v-app>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <v-dialog v-model="maintenance_dialog"
                    persistent max-width="500px"
                    ref="addMaintenanceDialog"
                    @keydown.esc="maintenance_dialog = false"
          >
            <template v-slot:activator="{ on }">
              <v-btn color="secondary" dark v-on="on">Add maintenance entry</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">Add maintenance entry</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="8">
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
                    <v-col cols="12" sm="6" md="4">
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
                    <v-col cols="12" sm="6" md="8">
                      <v-select :items="['Motor', 'Carburetor', 'Attachments', 'Brakes', 'Clutch',
                      'Suspension', 'Wheels']"
                                label="Category name*"
                                required
                                v-model="history_form_dict.category">
                      </v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        append-outer-icon="mdi-plus"
                        prepend-icon="mdi-minus"
                        @click:append-outer="increment"
                        @click:prepend="decrement"
                        required
                        hint="of engine operation"
                        suffix="h*"
                        v-model="history_form_dict.hours">
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-combobox
                        :items="maintenance_names_dict[history_form_dict.category]"
                        label="Maintenance*"
                        required
                        ref="NameComboBox"
                        v-model="history_form_dict.name">
                      </v-combobox>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field label="Comment"
                                    v-model="history_form_dict.comment">
                      </v-text-field>
                    </v-col>
                  </v-row>
                  <v-spacer></v-spacer>
                  <p class="text--secondary text-sm-right">
                    *indicates required field</p>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" text @click="onCancel">Close</v-btn>
                <v-btn color="secondary" text @click="onSubmit">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <br>
          <v-simple-table fixed-header height="500px">
            <thead>
            <tr>
              <th class="text-left">Category</th>
              <th class="text-left">Name</th>
              <th class="text-left">Hours</th>
              <th class="text-left">Date</th>
              <th class="text-left">Comment</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="(maintenance) in history_list" v-bind:key="maintenance.hist_id">
                <td>{{ maintenance.category }}</td>
                <td>{{ maintenance.name }}</td>
                <td>{{ maintenance.hours }}</td>
                <td>{{ maintenance.datetime_display | formatDateTime }}</td>
                <td>{{ maintenance.comment }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <v-btn color="warning" text @click="editHistory(maintenance.hist_id)">
                      Edit
                    </v-btn>
                    <v-dialog v-model="confirm_delete_dialog" persistent max-width="400">
                      <template v-slot:activator="{ on }">
                        <v-btn color="error" text v-on="on">
                          Delete
                        </v-btn>
                      </template>
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
                                 @click="deleteHistoryItem(maintenance.hist_id)">Delete</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'History',
  data() {
    return {
      history_list: [],
      history_form_dict: {
        hist_id: '',
        category: '',
        name: '',
        hours: '',
        date: new Date().toISOString().substr(0, 10),
        time: new Date().toTimeString().substr(0, 5),
        comment: '',
      },
      maintenance_names_dict: {
        Motor: ['Motor 1', 'Motor 2'],
        Carburetor: ['Carburetor 1', 'Carburetor 2'],
        Attachments: ['Attachments 1', 'Attachments 2'],
        Brakes: ['Brakes 1', 'Brakes 2'],
        Clutch: ['Clutch 1', 'Clutch 2'],
        Suspension: ['Suspension 1', 'Suspension 2'],
        Wheels: ['Wheels 1', 'Wheels 2'],
      },
      edit: false,
      maintenance_dialog: false,
      confirm_delete_dialog: false,
      date_menu: false,
      time_menu: false,
    };
  },
  methods: {
    getHistory() {
      const path = '/api/maintenance/history';
      axios.get(path)
        .then((res) => {
          this.history_list = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    postHistory(payload) {
      const path = '/api/maintenance/history';
      axios.post(path, payload)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.log(error);
          this.getHistory();
        });
    },
    getMaintenance() {
      const path = '/api/maintenance/list';
      axios.get(path)
        .then((res) => {
          this.maintenance_names_dict = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    initForm() {
      this.history_form_dict.hist_id = '';
      this.history_form_dict.category = '';
      this.history_form_dict.name = '';
      this.history_form_dict.date = '';
      this.history_form_dict.time = '';
      this.history_form_dict.hours = '';
      this.history_form_dict.comment = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.NameComboBox.blur();
      this.$nextTick(() => {
        const datetime = this.history_form_dict.date.concat('T', this.history_form_dict.time);
        const payload = {
          category: this.history_form_dict.category,
          name: this.history_form_dict.name,
          hours: this.history_form_dict.hours,
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
      this.history_form_dict.hours = Number(parseFloat(this.history_form_dict.hours) + 0.1)
        .toFixed(1);
    },
    decrement() {
      this.history_form_dict.hours = Number(parseFloat(this.history_form_dict.hours) - 0.1)
        .toFixed(1);
    },
    editHistory(MtnId) {
      const path = `/api/maintenance/history/${MtnId}`;
      axios.get(path)
        .then((res) => {
          this.history_form_dict.hist_id = res.data.hist_id;
          this.history_form_dict.category = res.data.category;
          this.history_form_dict.name = res.data.name;
          this.history_form_dict.hours = res.data.hours;
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
      const path = `/api/maintenance/history/${this.history_form_dict.hist_id}`;
      axios.put(path, payload)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.log(error);
          this.getHistory();
        });
      this.edit = false;
    },
    deleteHistoryItem(MtnID) {
      const path = `/api/maintenance/history/${MtnID}`;
      axios.delete(path)
        .then(() => {
          this.getHistory();
        })
        .catch((error) => {
          console.log(error);
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
    this.getMaintenance();
  },
};
</script>
