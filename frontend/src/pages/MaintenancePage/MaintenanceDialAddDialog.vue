<template>
  <MaintenanceDialog
    :task="'Add'"
    :maintenance-dialog.sync="add_maintenance_dialog"
    :category-name.sync="category_name"
    :maintenance-name.sync="maintenance_name"
    :maintenance-object.sync="maintenance_object"
    :category-names="category_names"
    :maintenance-names="maintenance_names"
    @saveClicked="postMaintenanceItem"
    @cancelClicked="initMaintenanceObject"
  />
</template>

<script>
import { apiPostMaintenance } from '../../components/api/MaintenanceApi';
import MaintenanceDialog from './MaintenanceDialog.vue';

export default {
  name: 'MaintenanceDialAddDialog',
  components: {
    MaintenanceDialog,
  },
  props: {
    addMaintenanceDialog: {
      type: Boolean,
      required: true,
    },
    categoryArray: {
      type: Array,
      required: true,
    },
    categoryName: {
      type: String,
      required: true,
    },
    categoryNames: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    category_name: null,
    maintenance_name: null,
    maintenance_object: {
      bike_id: null,
      category: '',
      name: '',
      interval_type: null,
      interval_amount: null,
      interval_unit: null,
      tags_default: null,
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
  computed: {
    add_maintenance_dialog: {
      get() {
        return this.addMaintenanceDialog;
      },
      set(value) {
        this.$emit('update:addMaintenanceDialog', value);
      },
    },
    maintenance_names() {
      return this.categoryArray.map((value) => value.name);
    },
    category_names() {
      return this.categoryNames;
    },
    current_bike_id() {
      return this.$store.getters.getCurrentBikeId;
    },
  },
  created() {
    this.category_name = this.categoryName;
    this.maintenance_name = '';
  },
  methods: {
    /**
     * Posts a new maintenance item.
     */
    postMaintenanceItem() {
      this.maintenance_object.category = this.category_name;
      this.maintenance_object.name = this.maintenance_name;
      this.maintenance_object.bike_id = this.current_bike_id;
      const payload = this.maintenance_object;
      apiPostMaintenance(payload)
        .then((res) => {
          const index = this.categoryArray.indexOf(this.categoryArray.filter(
            (i) => i.name === this.maintenance_name,
          )[0]);
          this.categoryArray[index] = {
            category: payload.category,
            name: payload.name,
            interval_type: payload.interval_type,
            interval_amount: payload.interval_amount,
            interval_unit: payload.interval_unit,
          };
          this.categoryArray[index].maintenance_id = res.data;
          this.add_maintenance_dialog = false;
          this.initMaintenanceObject();
          this.$emit('newMaintenanceAdded');
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Maintenance entry added!',
          });
        })
        .catch((error) => {
          this.add_maintenance_dialog = false;
          this.initMaintenanceObject();
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    /**
     * Initializes the object for the add maintenance dialog form.
     */
    initMaintenanceObject() {
      this.maintenance_object.maintenance_id = null;
      this.maintenance_object.bike_id = null;
      this.maintenance_object.category = '';
      this.maintenance_object.name = '';
      this.maintenance_object.interval_type = null;
      this.maintenance_object.interval_amount = null;
      this.maintenance_object.interval_unit = null;
      this.maintenance_object.tags_default = null;
    },
  },
};
</script>
