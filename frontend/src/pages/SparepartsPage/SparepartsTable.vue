<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="sparepart_items"
      :search="spareparts_search"
      :expanded.sync="expanded"
      :footer-props="{ itemsPerPageText: '' }"
      @click:row="expandRow"
    >
      <template v-slot:expanded-item="props">
        <td :colspan="window_width">
          <tr
            v-for="(item) in props.item.items"
            :key="item.sparepartitem_id"
          >
            <td style="min-width: 115px; width: 7000px">
              {{ item.description }}
            </td>
            <td style="min-width: 95px; width: 3000px">
              {{ item.condition }}
            </td>
            <td style="min-width: 75px">
              <v-btn
                color="warning"
                icon
                @click.prevent="onEditButton(item.sparepartitem_id)"
              >
                <v-icon>mdi-square-edit-outline</v-icon>
              </v-btn>
              <v-btn
                color="error"
                icon
                @click.prevent="onDeleteButton(item.sparepartitem_id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </td>
      </template>
    </v-data-table>
    <v-card-text style="height: 5px; position: relative">
      <v-btn
        class="mt-n7"
        absolute
        x-small
        fab
        top
        left
        color="primary"
        @click.prevent="sparepart_dialog = true"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-card-text>
    <SparepartsDialogForm
      :bike-modules="bikeModules"
      :spareparts-dialog.sync="sparepart_dialog"
      @saveButtonClicked="$emit('refreshSpareParts')"
    />
    <ConfirmDeleteDialog
      :flagged-for-deletion="'spare part entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import { apiDeleteSparepartitemItem } from '../../components/api/SparepartitemApi';
import SparepartsDialogForm from './SparepartsDialogForm.vue';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';

export default {
  name: 'SparepartsTable',
  components: {
    ConfirmDeleteDialog,
    SparepartsDialogForm,
  },
  props: {
    sparepartItems: {
      type: Array,
      required: true,
    },
    sparepartsSearch: {
      type: String,
      required: true,
    },
    bikeModules: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    headers: [
      {
        text: 'Part',
        align: 'start',
        sortable: true,
        value: 'name',
      },
      {
        text: 'Stock',
        align: 'start',
        sortable: false,
        value: 'current_stock',
      },
      {
        text: 'Warn at',
        align: 'start',
        sortable: false,
        value: 'min_stock',
      },
    ],
    expanded: [],
    sparepartitem_id: null,
    sparepart_dialog: false,
    confirm_delete_dialog: false,
  }),
  computed: {
    sparepart_items() {
      return this.sparepartItems;
    },
    spareparts_search: {
      get() {
        return this.sparepartsSearch;
      },
      set(value) {
        this.$emit('update:sparepartsSearch', value);
      },
    },
  },
  updated() {
    this.window_width = window.innerWidth;
  },
  created() {
    this.window_width = window.innerWidth;
  },
  methods: {
    expandRow(item) {
      this.expanded = item === this.expanded[0] ? [] : [item];
    },
    onEditButton(sparepartitemId) {
      this.$emit('editButtonClicked', sparepartitemId);
    },
    onDeleteButton(sparepartitemId) {
      this.sparepartitem_id = sparepartitemId;
      this.confirm_delete_dialog = true;
    },
    deletionConfirmed() {
      apiDeleteSparepartitemItem(this.sparepartitem_id)
        .then(() => {
          this.$emit('deletionConfirmed', this.sparepartitem_id);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: 'Spare part entry deleted!',
          });
        })
        .catch((error) => {
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
