<template>
  <div>
    <v-speed-dial
      :key="categoryName + '/speed_dial'"
      open-on-hover
      absolute
      top
      right
      direction="left"
      transition="slide-x-reverse-transition"
    >
      <template v-slot:activator>
        <v-btn
          icon
          outlined
          color="primary"
        >
          <v-icon>mdi-wrench</v-icon>
        </v-btn>
      </template>
      <v-btn
        fab
        dark
        x-small
        color="error"
      >
        <v-icon @click.prevent="deleteMaintenance()">
          mdi-delete
        </v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        x-small
        color="success"
      >
        <v-icon @click.prevent="editMaintenance()">
          mdi-pencil
        </v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        x-small
        color="secondary"
      >
        <v-icon @click.prevent="addMaintenance()">
          mdi-plus
        </v-icon>
      </v-btn>
    </v-speed-dial>
    <MaintenanceDialAddDialog
      :add-maintenance-dialog.sync="add_maintenance_dialog"
      :category-object="categoryObject"
      :category-name="categoryName"
      @newMaintenanceAdded="newMaintenanceAdded()"
    />
    <MaintenanceDialEditDialog
      :edit-maintenance-dialog.sync="edit_maintenance_dialog"
      :category-object="categoryObject"
      :category-name="categoryName"
    />
    <MaintenanceDialDeleteDialog
      :delete-maintenance-dialog.sync="delete_maintenance_dialog"
      :category-object="categoryObject"
      :category-name="categoryName"
      @maintenanceDeleted="maintenanceDeleted()"
    />
  </div>
</template>

<script>
import MaintenanceDialAddDialog from './MaintenanceDialAddDialog.vue';
import MaintenanceDialEditDialog from './MaintenanceDialEditDialog.vue';
import MaintenanceDialDeleteDialog from './MaintenanceDialDeleteDialog.vue';

export default {
  name: 'MaintenanceDial',
  components: {
    MaintenanceDialDeleteDialog,
    MaintenanceDialEditDialog,
    MaintenanceDialAddDialog,
  },
  props: {
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
    add_maintenance_dialog: false,
    edit_maintenance_dialog: false,
    delete_maintenance_dialog: false,
  }),
  methods: {
    addMaintenance() {
      this.add_maintenance_dialog = true;
    },
    editMaintenance() {
      this.edit_maintenance_dialog = true;
    },
    deleteMaintenance() {
      this.delete_maintenance_dialog = true;
    },
    newMaintenanceAdded() {
      this.$emit('newMaintenanceAdded');
    },
    maintenanceDeleted() {
      this.$emit('maintenanceDeleted');
    },
  },
};
</script>

<style scoped>

</style>
