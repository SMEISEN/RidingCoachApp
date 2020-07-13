<template>
  <v-dialog
    v-model="addMaintenanceDialog"
    persistent
    max-width="500px"
  >
    <v-form
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add maintenance interval: {{ categoryName }}</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model="new_maintenance.name"
                :rules="[v => !!v]"
                label="Maintenance name"
                required
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="4"
              md="4"
            >
              <v-select
                v-model="new_maintenance.interval_type"
                :items="interval_types"
                :rules="[v => !!v]"
                label="Interval type"
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
                v-model.number="new_maintenance.interval_amount"
                :rules="[v => !!v]"
                label="Interval amount"
                required
              />
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="4"
              md="4"
            >
              <v-select
                v-model="new_maintenance.interval_unit"
                :items="interval_units"
                :rules="[v => !!v]"
                label="Interval unit"
                required
              />
            </v-col>
          </v-row>
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
import { apiPostMaintenance } from '../../components/api/MaintenanceApi';

export default {
  name: 'MaintenanceDialAddDialog',
  props: {
    addMaintenanceDialog: {
      type: Boolean,
      required: true,
    },
    categoryObject: {
      type: Object,
      required: true,
    },
    categoryName: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    valid: true,
    new_maintenance: {
      category: null,
      name: null,
      interval_type: null,
      interval_amount: null,
      interval_unit: null,
    },
    interval_types: [
      'planned cycle',
      'estimated wear',
    ],
    interval_units: [
      'h',
      'a',
      't',
    ],
  }),
  created() {
    this.new_maintenance.category = this.categoryName;
  },
  updated() {
  },
  methods: {
    onSave() {
      const payload = this.new_maintenance;
      const maintenanceName = this.new_maintenance.name;
      this.categoryObject[maintenanceName] = {
        name: this.new_maintenance.name,
        interval_type: this.new_maintenance.interval_type,
        interval_amount: this.new_maintenance.interval_amount,
        interval_unit: this.new_maintenance.interval_unit,
      };
      apiPostMaintenance(payload).then((res) => {
        this.categoryObject[maintenanceName].maintenance_id = res.data;
        this.$emit('update:addMaintenanceDialog', false);
        this.$emit('newMaintenanceAdded');
      });
    },
    onCancel() {
      this.$emit('update:addMaintenanceDialog', false);
    },
  },
};
</script>

<style scoped>

</style>
