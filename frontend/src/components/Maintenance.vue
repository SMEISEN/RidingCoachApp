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
                      <v-text-field label="Category name*"
                                    required
                                    v-model="addMaintenanceForm.category">
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                      <v-text-field
                        label="Hours*"
                        required
                        hint="of engine operation"
                        v-model="addMaintenanceForm.hours">
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field label="Maintenance*" required
                                    v-model="addMaintenanceForm.name">
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field label="Comment"
                                    v-model="addMaintenanceForm.comment">
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
              <tr v-for="(maintenance, index) in maintenance_list" :key="index">
                <td>{{ maintenance.category }}</td>
                <td>{{ maintenance.name }}</td>
                <td>{{ maintenance.hours }}</td>
                <td>{{ maintenance.date }}</td>
                <td>{{ maintenance.comment }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <v-btn color="warning" text @click="">Edit</v-btn>
                    <v-btn color="success" text @click="">Done!</v-btn>
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
      maintenance_list: [],
      addMaintenanceForm: {
        category: '',
        name: '',
        hours: '',
        date: '',
        comment: '',
      },
      dialog: false,
    };
  },
  methods: {
    getMaintenance() {
      const path = '/api/maintenance/history';
      axios.get(path)
        .then((res) => {
          this.maintenance_list = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addMaintenance(payload) {
      const path = '/api/maintenance/history';
      axios.post(path, payload)
        .then(() => {
          this.getMaintenance();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMaintenance();
        });
    },
    initForm() {
      this.addMaintenanceForm.category = '';
      this.addMaintenanceForm.name = '';
      this.addMaintenanceForm.hours = '';
      this.addMaintenanceForm.date = '';
      this.addMaintenanceForm.comment = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.dialog = false;
      const payload = {
        category: this.addMaintenanceForm.category,
        name: this.addMaintenanceForm.name,
        hours: this.addMaintenanceForm.hours,
        date: this.addMaintenanceForm.date,
        comment: this.addMaintenanceForm.comment,
      };
      this.addMaintenance(payload);
      this.initForm();
    },
    onCancel(evt) {
      evt.preventDefault();
      this.dialog = false;
      this.initForm();
    },
  },
  created() {
    this.getMaintenance();
  },
};
</script>
