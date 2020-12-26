<template>
  <v-dialog
    v-model="maintenance_dialog"
    persistent
    max-width="500px"
  >
    <v-form
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">{{ task }} maintenance interval</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-combobox
                v-model="category_name"
                :items="categoryArray"
                :rules="[v => !!v]"
                label="Category name"
                required
              />
            </v-col>
          </v-row>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-select
                v-if="task === 'Edit'"
                v-model="maintenance_name"
                :items="maintenanceArray"
                :rules="[v => !!v]"
                label="Maintenance name"
                required
              />
              <v-text-field
                v-if="task === 'Add'"
                v-model="maintenance_name"
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
                v-model="maintenance_object.interval_type"
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
                v-model.number="maintenance_object.interval_amount"
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
                v-model="maintenance_object.interval_unit"
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
export default {
  name: 'MaintenanceDialog',
  props: {
    task: {
      type: String,
      required: true,
    },
    maintenanceDialog: {
      type: Boolean,
      required: true,
    },
    categoryName: {
      type: String,
      required: true,
    },
    maintenanceName: {
      type: String,
      required: true,
    },
    maintenanceObject: {
      type: Object,
      required: true,
    },
    categoryArray: {
      type: Array,
      required: true,
    },
    maintenanceArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    valid: true,
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
  computed: {
    maintenance_object: {
      get() {
        return this.maintenanceObject;
      },
      set(value) {
        this.$emit('update:maintenanceObject', value);
      },
    },
    maintenance_name: {
      get() {
        return this.maintenanceName;
      },
      set(value) {
        this.$emit('update:maintenanceName', value);
      },
    },
    category_name: {
      get() {
        return this.categoryName;
      },
      set(value) {
        this.$emit('update:categoryName', value);
      },
    },
    maintenance_dialog: {
      get() {
        return this.maintenanceDialog;
      },
      set(value) {
        this.$emit('update:maintenanceDialog', value);
      },
    },
  },
  methods: {
    onSave() {
      this.$emit('saveClicked');
    },
    onCancel() {
      this.maintenance_dialog = false;
    },
  },
};
</script>

<style scoped>

</style>
