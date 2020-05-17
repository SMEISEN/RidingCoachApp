<template v-slot:default>
  <v-app>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <v-dialog v-model="dialog"
                    persistent max-width="600px"
                    ref="addMaintenanceDialog"
                    @keydown.esc="dialog = false">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark v-on="on">Add maintenance</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">Add maintenance</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="9">
                      <v-select :items="['Motor', 'Carburetor', 'Attachments', 'Brakes',
                      'Clutch', 'Suspension', 'Wheels']"
                                    label="Category name*"
                                    required
                                    v-model="history_form_dict.category">
                      </v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Hours*"
                        required
                        hint="of engine operation"
                        v-model="history_form_dict.hours">
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-combobox
                        :items="maintenance_names_dict[history_form_dict.category]"
                        label="Maintenance*"
                        required
                        v-model="history_form_dict.name">
                      </v-combobox>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field label="Comment"
                                    v-model="history_form_dict.comment">
                      </v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="secondary" text @click="onCancel">Close</v-btn>
                <v-btn color="secondary" text @click="onSubmit">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <br>
          <v-simple-table fixed-header height="300px">
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
              <tr v-for="(maintenance, index) in history_list" :key="index">
                <td>{{ maintenance.category }}</td>
                <td>{{ maintenance.name }}</td>
                <td>{{ maintenance.hours }}</td>
                <td>{{ maintenance.date }}</td>
                <td>{{ maintenance.comment }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <v-btn color="warning" text @click="dialog = false">Edit</v-btn>
                    <v-btn color="success" text @click="dialog = false">Done!</v-btn>
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
  data() {
    return {
      history_list: [],
      history_form_dict: {
        category: '',
        name: '',
        hours: '',
        date: '',
        comment: '',
      },
      dialog: false,
      maintenance_names_dict: {
        Motor: [],
        Carburetor: [],
        Attachments: [],
        Brakes: [],
        Clutch: [],
        Suspension: [],
        Wheels: [],
      },
    };
  },
  methods: {
    getMaintenanceHistory() {
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
    getMaintenanceNames() {
      const path = '/api/maintenance/list';
      axios.get(path)
        .then((res) => {
          this.maintenance_names_dict = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addMaintenanceHistory(payload) {
      const path = '/api/maintenance/history';
      axios.post(path, payload)
        .then(() => {
          this.getMaintenanceHistory();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMaintenanceHistory();
        });
    },
    initForm() {
      this.history_form_dict.category = '';
      this.history_form_dict.name = '';
      this.history_form_dict.hours = '';
      this.history_form_dict.date = '';
      this.history_form_dict.comment = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.dialog = false;
      const payload = {
        category: this.history_form_dict.category,
        name: this.history_form_dict.name,
        hours: this.history_form_dict.hours,
        date: this.history_form_dict.date,
        comment: this.history_form_dict.comment,
      };
      this.addMaintenanceHistory(payload);
      this.initForm();
    },
    onCancel(evt) {
      evt.preventDefault();
      this.dialog = false;
      this.initForm();
    },
  },
  created() {
    this.getMaintenanceHistory();
    this.getMaintenanceNames();
  },
};
</script>
