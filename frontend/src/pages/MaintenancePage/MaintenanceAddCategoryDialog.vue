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
      :category-array="category_array"
      :category-name="category_name"
      :category-names="category_names"
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
    categoryNames: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    add_maintenance_dialog: false,
    category_array: [],
    category_name: '',
  }),
  computed: {
    category_names() {
      return this.categoryNames;
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
