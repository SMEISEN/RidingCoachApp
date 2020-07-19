<template>
  <v-dialog
    v-model="editMaintenanceDialog"
    persistent
    max-width="500px"
  >
    <v-form
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Edit maintenance interval: {{ categoryName }}</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-select
                v-model="selected_name"
                :items="Object.keys(categoryObject)"
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
                v-model="categoryObject[selected_name].interval_type"
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
                v-model.number="categoryObject[selected_name].interval_amount"
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
                v-model="categoryObject[selected_name].interval_unit"
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
import { apiPutMaintenanceItem } from '../../components/api/MaintenanceApi';

export default {
  name: 'MaintenanceDialEditDialog',
  props: {
    editMaintenanceDialog: {
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
    selected_name: null,
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
    [this.selected_name] = Object.keys(this.categoryObject);
  },
  updated() {
  },
  methods: {
    onSave() {
      const mtnId = this.categoryObject[this.selected_name].maintenance_id;
      const payload = {
        interval_amount: this.categoryObject[this.selected_name].interval_amount,
        interval_unit: this.categoryObject[this.selected_name].interval_unit,
        interval_type: this.categoryObject[this.selected_name].interval_type,
      };
      apiPutMaintenanceItem(payload, mtnId)
        .then(() => {
          this.$emit('update:editMaintenanceDialog', false);
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    onCancel() {
      this.$emit('update:editMaintenanceDialog', false);
    },
  },
};
</script>

<style scoped>

</style>
