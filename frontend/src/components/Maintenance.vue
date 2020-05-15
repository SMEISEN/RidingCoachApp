<template v-slot:default>
  <v-app>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Maintenance</h1>
          <hr><br><br>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.maintenance-modal>
            Add Maintenance
          </button>
          <br><br>
          <v-simple-table fixed-header height="300px">
            <thead>
            <tr>
              <th class="text-left">Category</th>
              <th class="text-left">Name</th>
              <th class="text-left">Interval</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="(maintenance, index) in maintenance_list" :key="index">
                <td>{{ maintenance.category }}</td>
                <td>{{ maintenance.name }}</td>
                <td>{{ maintenance.hours_interval }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-warning btn-sm">Done!</button>
                    <button type="button" class="btn btn-danger btn-sm">Edit</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </div>
      </div>
      <b-modal ref="addMaintenanceModal"
                     id="maintenance-modal"
                     title="Add a new maintenance"
                     hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-category-group"
                        label="Category:"
                        label-for="form-category-input">
            <b-form-input id="form-category-input"
                          type="text"
                          v-model="addMaintenanceForm.category"
                          required
                          placeholder="Enter category name">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-name-group"
                        label="Name:"
                        label-for="form-name-input">
            <b-form-input id="form-name-input"
                          type="text"
                          v-model="addMaintenanceForm.name"
                          required
                          placeholder="Enter maintenance name">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-interval-group"
                        label="Interval:"
                        label-for="form-interval-input">
            <b-form-input id="form-interval-input"
                          type="text"
                          v-model="addMaintenanceForm.hours_interval"
                          required
                          placeholder="Enter interval hours">
            </b-form-input>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
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
        hours_interval: '',
      },
    };
  },
  methods: {
    getMaintenance() {
      const path = 'http://localhost:5000/api/maintenance/list';
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
      const path = 'http://localhost:5000/api/maintenance/new';
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
      this.addMaintenanceForm.hours_interval = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addMaintenanceModal.hide();
      const payload = {
        category: this.addMaintenanceForm.category,
        name: this.addMaintenanceForm.name,
        hours_interval: this.addMaintenanceForm.hours_interval,
      };
      this.addMaintenance(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addMaintenanceModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getMaintenance();
  },
};
</script>
