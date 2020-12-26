<template>
  <MaintenanceDialog
    :task="'Edit'"
    :maintenance-dialog.sync="edit_maintenance_dialog"
    :category-name.sync="category_name"
    :maintenance-name.sync="maintenance_name"
    :maintenance-object="maintenance_object"
    :category-list="category_list"
    :maintenance-list="maintenance_list"
    @saveClicked="putMaintenanceItem"
  />
</template>

<script>
import { apiPutMaintenanceItem } from '../../components/api/MaintenanceApi';
import MaintenanceDialog from './MaintenanceDialog.vue';

export default {
  name: 'MaintenanceDialEditDialog',
  components: {
    MaintenanceDialog,
  },
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
    maintenance_name: null,
  }),
  computed: {
    edit_maintenance_dialog: {
      get() {
        return this.editMaintenanceDialog;
      },
      set(value) {
        this.$emit('update:editMaintenanceDialog', value);
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
    maintenance_object: {
      get() {
        return this.categoryObject[this.maintenance_name];
      },
      set(value) {
        this.$emit('update:categoryName', value);
      },
    },
    maintenance_list() {
      return Object.keys(this.categoryObject);
    },
    category_list() {
      return Object.keys(this.categoryObject);
    },
  },
  created() {
    [this.maintenance_name] = this.category_list;
  },
  updated() {
  },
  methods: {
    putMaintenanceItem() {
      const mtnId = this.maintenance_object.maintenance_id;
      const payload = {
        interval_amount: this.maintenance_object.interval_amount,
        interval_unit: this.maintenance_object.interval_unit,
        interval_type: this.maintenance_object.interval_type,
      };
      apiPutMaintenanceItem(payload, mtnId)
        .then(() => {
          this.edit_maintenance_dialog = false;
        })
        .catch((error) => {
          this.edit_maintenance_dialog = false;
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>

<style scoped>

</style>
