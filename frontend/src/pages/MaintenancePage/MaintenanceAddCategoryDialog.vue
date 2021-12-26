<template>
  <v-col
    cols="12"
    xs="12"
    sm="12"
    md="6"
  >
    <v-card
      class="card-container"
      height="365px"
    >
      <v-container
        class="justify-center"
        fill-height
      >
        <v-btn
          icon
          x-large
          outlined
          @click.prevent="addNewMaintenanceCategory"
        >
          <v-icon>
            mdi-plus
          </v-icon>
        </v-btn>
      </v-container>
    </v-card>
    <MaintenanceDialAddDialog
      :add-maintenance-dialog.sync="add_maintenance_dialog"
      :category-object="category_object"
      :category-name="category_name"
      :category-array="category_array"
      @newMaintenanceAdded="$emit('refreshTable')"
    />
  </v-col>
</template>

<script>
import MaintenanceDialAddDialog from './MaintenanceDialAddDialog.vue';

export default {
  name: 'MaintenanceAddCategoryDialog',
  components: {
    MaintenanceDialAddDialog,
  },
  props: {
    categoryArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    add_maintenance_dialog: false,
    category_object: {},
    category_name: '',
  }),
  computed: {
    category_array() {
      return this.categoryArray;
    },
  },
  methods: {
    /**
     * Opens the add maintenance dialog.
     */
    addNewMaintenanceCategory() {
      this.add_maintenance_dialog = true;
    },
  },
};
</script>

<style scoped>

</style>
