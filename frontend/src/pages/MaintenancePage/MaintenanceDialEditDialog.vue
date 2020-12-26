<template>
  <MaintenanceDialog
    :task="'Edit'"
    :maintenance-dialog.sync="edit_maintenance_dialog"
    :category-name.sync="category_name"
    :maintenance-name.sync="maintenance_name"
    :maintenance-object.sync="maintenance_object"
    :category-array="category_array"
    :maintenance-array="maintenance_array"
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
    categoryArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    category_name: null,
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
    maintenance_object() {
      return this.categoryObject[this.maintenance_name];
    },
    maintenance_array() {
      return Object.keys(this.categoryObject);
    },
    category_array() {
      return this.categoryArray;
    },
  },
  created() {
    this.category_name = this.categoryName;
    [this.maintenance_name] = this.maintenance_array;
  },
  methods: {
    putMaintenanceItem() {
      const mtnId = this.maintenance_object.maintenance_id;
      this.maintenance_object.category = this.category_name;
      this.maintenance_object.name = this.maintenance_name;
      const payload = this.maintenance_object;
      apiPutMaintenanceItem(payload, mtnId)
        .then(() => {
          this.edit_maintenance_dialog = false;
          this.$emit('maintenanceEdited');
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Maintenance entry edited!',
          });
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
